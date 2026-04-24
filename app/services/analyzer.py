import fitz
import torch
import logging
import json
import asyncio
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
        
        # 가드레일 전용 프롬프트
        self.GUARDRAIL_PROMPT = """
        너는 법률 계약 검토 서비스 'ANTIDOTE'의 안내원이야. 
        사용자 입력이 '근로계약', '노동법', '고용 관계', '약관 분석'과 관련이 있는지 판단해줘.
        - 관련 없음: {"is_valid": false, "guide_message": "죄송합니다. Antidote는 근로계약 및 불공정 약관 분석 전문 서비스입니다. 관련 조항이나 법률 질문을 입력해 주세요."}
        - 관련 있음: {"is_valid": true}
        JSON으로만 응답해.
        """

    async def _check_validity(self, text: str):
        if not self.client: return {"is_valid": True}
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{self.GUARDRAIL_PROMPT}\n\n사용자 입력: {text}",
                config={"temperature": 0.1, "response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Guardrail Error: {e}")
            return {"is_valid": True}

    async def _generate_llm_report(self, clause: str, law: Any, precedent: Any) -> Dict[str, Any]:
        """단일 법령 및 판례 객체를 받아 구조화된 JSON 리포트 생성"""
        
        # 리스트가 아닌 단일 객체에서 데이터를 추출합니다.
        law_info = f"{law.keyword}: {law.summary}" if law else "관련 법령 정보 없음"
        pre_info = f"{precedent.case_number}: {precedent.content}" if precedent else "관련 판례 정보 없음"

        prompt = f"""
        당신은 대한민국 최고의 법률 AI 'Antidote'입니다.
        다음 [검토 조항]을 [참고 데이터]에 근거하여 분석하고 반드시 지정된 JSON 형식으로만 답변하세요.

        [검토 조항]
        "{clause}"

        [참고 데이터]
        - 관련 법령: {law_info}
        - 관련 판례: {pre_info}

        [출력 JSON 형식]
        {{
            "reason": "위반 내용과 이유를 50자 이내로 기술",
            "proposed_text": "리스크를 제거한 표준형 조항 문장"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.1, "response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"LLM JSON Generation Error: {e}")
            return {"risk_level": "알 수 없음", "reason": "분석 중 오류가 발생했습니다.", "proposed_text": ""}

    async def analyze(self, text: str, doc_name: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 0. 가드레일
        validity = await self._check_validity(text)
        if not validity.get("is_valid", True):
            return {"status": "invalid_query", "message": validity.get("guide_message"), "results": []}

        chunks = self.processor.smart_chunking(text)
        analysis_results = []
        all_scores = []
        
        small_model, small_tokenizer = ml_engine.get_small_model()
        base_model, base_tokenizer = ml_engine.get_base_model()
        device = ml_engine.device

        for item in chunks:
            original = item['original']
            embedding_text = item['for_embedding']

            # 1. KoELECTRA 위험 탐지
            inputs = small_tokenizer(original, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
            with torch.no_grad():
                probs = F.softmax(small_model(**inputs).logits, dim=-1)
                confidence = probs[0][1].item() * 100
            
            all_scores.append(confidence)

            # 2. RAG 기반 데이터 검색 및 재랭킹
            refined_laws, refined_precedents = [], []
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
                    refined_laws = law_scores[0][1] if law_scores else None

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
                    refined_precedents = pre_scores[0][1] if pre_scores else None

            # 3. 수정본 생성 (주의 이상 조항일 경우에만)
            if confidence >= 40:
                # 텍스트가 아닌 JSON 객체를 받아옴
                report_data = await self._generate_llm_report(original, refined_laws, refined_precedents)
                
                analysis_results.append({
                    "clause": original,
                    "level": "EXTREME" if confidence >= 80 else "DANGER" if confidence >= 60 else "WARNING",
                    "score": round(confidence, 2),
                    # 프론트에서 즉시 사용 가능하도록 개별 필드 매핑
                    "reason": report_data.get("reason", "분석 실패"),
                    "proposed_text": report_data.get("proposed_text", ""),
                    "tags": ["#부당계약", "#검토필요"],
                    "legal_basis": [{"title": refined_laws.keyword, "summary": refined_laws.summary}] if refined_laws else [],
                    "precedents": [{"title": refined_precedents.case_number, "content": refined_precedents.content}] if refined_precedents else []
                })
            else:
                analysis_results.append({
                    "clause": original,
                    "level": "CAUTION" if confidence >= 20 else "SAFE",
                    "score": round(confidence, 2),
                    "reason": "관련 법령 위반 사항이 발견되지 않았습니다.",
                    "proposed_text": "",
                    "tags": ["#안전"],
                    "legal_basis": [],
                    "precedents": []
                })

        return {
            "status": "success",
            "doc_name": doc_name,
            "results": analysis_results,
            "total_risk_score": round(sum(all_scores) / len(all_scores), 2) if all_scores else 0,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    async def analyze_pdf(self, file_content: bytes, filename: str):
        full_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"
        refined_text = self.processor.clean_pdf_text(full_text)
        return await self.analyze(refined_text, filename)