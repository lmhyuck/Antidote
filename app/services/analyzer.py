import fitz
import torch
import logging
import json
from google import genai
import torch.nn.functional as F
from datetime import datetime
from typing import Dict, Any

from app.core.model_loader import ml_engine
from .text_processor import TextProcessor
from .db_search import DBSearch
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")

class LegalAnalyzer:
    def __init__(self):
        self.processor = TextProcessor()
        self.db_search = DBSearch()
        self.client, self.model_name = ml_engine.get_gemini_client()
        
        self.SYSTEM_PROMPT = """
        너는 법률 계약 검토 서비스 'ANTIDOTE'의 안내원이야. 
        입력된 텍스트가 '계약서 조항 분석'이나 '법률적 위험도 확인'과 관련이 있는지 판단해줘.

        [판단 기준]
        1. 계약서 조항(임금, 해고, 비밀유지 등)이거나 법적 권리 질문인 경우: {"is_valid": true}
        2. 일상 대화, 맛집 질문, 단순 지식 질문인 경우: {"is_valid": false, "guide_message": "정중한 안내 텍스트"}

        가이드 메시지 예시: "ANTIDOTE는 계약서의 독소 조항을 분석하는 전문 서비스입니다. 분석을 원하시는 조항을 복사하여 입력해 주세요."
        반드시 JSON 형식으로만 응답해.
        """

    async def _check_validity(self, text: str):
        if not self.client:
            return {"is_valid": True}
            
        max_retries = 3
    
        for i in range(max_retries):
            try:
                # --- [수정] 신규 SDK 호출 문법 ---
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=f"{self.SYSTEM_PROMPT}\n\n사용자 입력: {text}",
                    config={
                        "temperature": 0.1,
                        "response_mime_type": "application/json"
                    }
                )
                # 신규 SDK는 결과값이 response.text에 담깁니다.
                return json.loads(response.text)
            except Exception as e:
                if "503" in str(e) and i < max_retries - 1:
                    logger.warning(f"서버 과부하로 재시도 중... ({i+1}/{max_retries})")
                    await asyncio.sleep(2) # 2초 대기 후 다시 시도
                    continue
                logger.error(f"Guardrail Error: {e}")
                return {"is_valid": True}

    async def analyze(self, text: str, doc_name: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 0. 가드레일 체크 (실패 시)
        validity = await self._check_validity(text)
        if not validity.get("is_valid", True):
            return {
                "status": "invalid_query",
                "message": validity.get("guide_message", "계약서 조항을 입력해 주세요."),
                "doc_name": doc_name,
                "total_risk_score": 0.0,
                "results": [],  # 프론트에서 map() 함수 에러 방지를 위해 빈 배열 유지
                "analyzed_at": now
            }

        # 1. 텍스트 청킹
        chunks = self.processor.smart_chunking(text)
        analysis_results = []
        all_scores = []
        
        # 모델 및 디바이스 설정
        small_model, small_tokenizer = ml_engine.get_small_model()
        base_model, base_tokenizer = ml_engine.get_base_model()
        device = ml_engine.device

        for item in chunks:
            original = item['original']
            embedding_text = item['for_embedding']

            # 2. KoELECTRA-Small 추론 (위험 탐지)
            inputs = small_tokenizer(original, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)

            with torch.no_grad():
                outputs = small_model(**inputs)
                probs = F.softmax(outputs.logits, dim=-1)
                confidence = probs[0][1].item() * 100
            
            all_scores.append(confidence)

            # 3. 판별 로직 (40점 기준 분기)
            if confidence >= 40:
                raw_laws, raw_precedents = self.db_search.get_related_data(embedding_text, top_k=10)
                
                # --- 중복 제거 로직 포함 정밀 검증 (Re-ranking) ---
                refined_laws = []
                seen_laws = set()
                if raw_laws:
                    law_scores = []
                    for law in raw_laws:
                        if law.keyword in seen_laws: continue # 중복 제거
                        
                        law_inputs = base_tokenizer(original, law.summary, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
                        with torch.no_grad():
                            law_outputs = base_model(**law_inputs)
                            law_probs = F.softmax(law_outputs.logits, dim=-1)
                            rel_score = law_probs[0][1].item()
                            law_scores.append((rel_score, law))
                            seen_laws.add(law.keyword)
                    
                    law_scores.sort(key=lambda x: x[0], reverse=True)
                    refined_laws = [item[1] for item in law_scores[:2]]

                refined_precedents = []
                seen_pre = set()
                if raw_precedents:
                    pre_scores = []
                    for pre in raw_precedents:
                        if pre.case_number in seen_pre: continue # 중복 제거

                        pre_inputs = base_tokenizer(original, pre.content, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
                        with torch.no_grad():
                            pre_outputs = base_model(**pre_inputs)
                            pre_probs = F.softmax(pre_outputs.logits, dim=-1)
                            rel_score = pre_probs[0][1].item()
                            pre_scores.append((rel_score, pre))
                            seen_pre.add(pre.case_number)
                    
                    pre_scores.sort(key=lambda x: x[0], reverse=True)
                    refined_precedents = [item[1] for item in pre_scores[:2]]

                analysis_results.append({
                    "clause": original,
                    "level": "DANGER" if confidence >= 70 else "WARNING",
                    "score": round(confidence, 2),
                    "description": f"해당 조항은 {refined_laws[0].keyword if refined_laws else '관련 법령'} 위반 소지가 있어 검토가 필요합니다.",
                    "tags": ["#부당계약", "#검토필요"],
                    "legal_basis": [{"title": l.keyword, "summary": l.summary} for l in refined_laws],
                    "precedents": [{"title": p.case_number, "content": p.content} for p in refined_precedents]
                })
            else:
                analysis_results.append({
                    "clause": original,
                    "level": "SAFE",
                    "score": round(confidence, 2),
                    "description": "해당 조항은 표준 근로계약 기준에 부합하며, 특별한 위험 요소가 발견되지 않았습니다.",
                    "tags": ["#안전", "#표준준수"],
                    "legal_basis": [],
                    "precedents": []
                })

        # 4. 전체 위험도 산출
        total_risk_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0

        return {
            "status": "success",
            "message": "분석이 성공적으로 완료되었습니다.",
            "doc_name": doc_name,
            "total_risk_score": total_risk_score,
            "results": analysis_results, 
            "analyzed_at": now
        }

    async def analyze_pdf(self, file_content: bytes, filename: str):
        full_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"
        refined_text = self.processor.clean_pdf_text(full_text)
        return await self.analyze(refined_text, filename)