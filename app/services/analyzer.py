import fitz
import torch
import logging
import json
import asyncio
import torch.nn.functional as F
from datetime import datetime
from typing import List, Dict, Any

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

    async def _split_and_classify_with_llm(self, text: str) -> List[Dict[str, str]]:
        """[신규] Gemini를 사용하여 텍스트를 의미 단위로 분리 및 유형 분류"""
        if not self.client: 
            return [{"text": text, "type": "GENERAL"}]

        prompt = f"""
        당신은 법률 상담 서비스의 전처리 전문가입니다.
        사용자가 입력한 다음 텍스트를 분석하여 '의미 단위'로 문장을 분리하고 유형을 분류하세요.
        입력이 하나라면 리스트에 하나만 담으세요.

        [분류 기준]
        1. GENERAL: 일반적인 궁금증, 법률 상식 질문, 노동법 관련 Q&A
        2. ANALYSIS: 실제 계약서의 조항 문구, 권리/의무가 명시된 구체적인 계약 내용

        [입력 텍스트]
        "{text}"

        [반환 형식]
        반드시 다음 JSON 리스트 형식으로만 답변하세요.
        [
            {{"text": "분리된 문장1", "type": "GENERAL"}},
            {{"text": "분리된 문장2", "type": "ANALYSIS"}}
        ]
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.1, "response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Split LLM Error: {e}")
            # 에러 시 대비책: 전체를 하나로 취급
            return [{"text": text, "type": "GENERAL"}]
        
    async def _get_simple_answer(self, question: str) -> Dict[str, Any]:
        """법률 관련 단순 질문에 대한 답변 생성"""
        prompt = f"""
        당신은 대한민국 최고의 법률 AI 'Antidote'입니다. 
        사용자의 법률 관련 질문에 대해 근로기준법을 바탕으로 정확하고 친절하게 답변하세요.

        [사용자 질문]
        "{question}"

        [임무]
        1. 질문의 핵심을 파악하여 2~3문장 내외로 명확하게 답변하세요.
        2. 답변의 근거가 되는 법령이 있다면 언급해 주세요.
        3. 답변은 "answer" 필드에 담으세요.

        [출력 JSON 형식]
        {{
            "answer": "답변 내용 (근거 법령 포함)"
        }}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.3, "response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Simple Answer Error: {e}")
            return {"answer": "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."}
        
    async def _generate_legal_report(self, clause: str, law: Any, precedent: Any) -> Dict[str, Any]:
        """리랭킹된 법령/판례를 바탕으로 정밀 독소 조항 분석 리포트 생성"""
        
        # 리랭킹 결과 반영
        law_info = f"[{law.keyword}] {law.summary}" if law else "근로기준법 원칙에 따라 분석 필요"
        pre_info = f"[{precedent.case_number}] {precedent.content}" if precedent else "관련 판례 없음"

        prompt = f"""
        당신은 대한민국 법률 분석 전문가입니다. 
        제시된 계약 조항의 위험성을 분석하고, 사용자를 보호하기 위한 수정안을 제시하세요.

        [분석 대상 조항]
        "{clause}"

        [참고 법률 데이터]
        - 핵심 법령: {law_info}
        - 관련 판례: {pre_info}

        [임무: 정밀 분석 및 검증]
        1. 분석: 참고 데이터를 바탕으로 해당 조항이 사용자(근로자)에게 불리한 이유를 'reason'에 기술하세요.
        2. 판례 검증: 제공된 판례가 해당 조항과 직접적으로 일치할 경우에만 'precedents' 리스트에 포함하세요. 
        만약 일치하지 않거나 부적절하다면 반드시 빈 리스트 []를 반환하세요.
        3. 법적 근거: 'legal_basis'에는 반드시 전달받은 [참고 데이터]의 법령 정보를 우선적으로 사용하세요. 
        전달받은 법령 데이터({law.keyword if law else '없음'})가 유효하다면 오직 그 1개의 데이터만 리스트에 담으세요. 
        본인의 판단 근거와 제공받은 [참고 데이터]의 법령 정보가 일치 하지 않은 경우에만 본인의 판단 근거로 사용한 법령 정보를 1개만 리스트에 담으세요.
        4. 대안 제시: 불리한 조항을 무효화하거나 완화할 수 있는 '표준 수정 문구'를 'proposed_text'에 작성하세요.

        [출력 JSON 형식]
        {{
            "reason": "판단 근거 (50자 이내)",
            "proposed_text": "수정 제안 문구",
            "legal_basis": [{{ "title": "조항명", "summary": "내용 요약" }}],
            "precedents": [{{ "title": "사건번호", "content": "판결 요지" }}]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.1, "response_mime_type": "application/json"} # 분석의 일관성을 위해 낮은 온도 설정
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Analysis Report Error: {e}")
            return {
                "reason": "데이터 처리 중 오류가 발생했습니다.", 
                "proposed_text": "전문가와 상담을 권장합니다.", 
                "legal_basis": [], 
                "precedents": []
            }

    async def analyze(self, text: str, doc_name: str, mode: str = "text"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 0. 가드레일 (서비스 관련성 체크)
        validity = await self._check_validity(text)
        if not validity.get("is_valid", True):
            return {"status": "invalid_query", "message": validity.get("guide_message"), "results": []}

    # [핵심] 입력 모드에 따른 문장 분리 전략 이원화
        if mode == "file":
            chunks = self.processor.smart_chunking(text)
            # TextProcessor는 'original' 키를 반환하므로 이를 'text'로 통일해서 변환
            parsed_items = [{"text": c['original'], "type": "ANALYSIS"} for c in chunks]
        else:
            # LLM은 이미 {'text': '...', 'type': '...'} 형식을 반환하도록 프롬프트에 정의됨
            parsed_items = await self._split_and_classify_with_llm(text)

        analysis_results = []
        all_scores = []
        
        # 모델 엔진 로드
        small_model, small_tokenizer = ml_engine.get_small_model()
        base_model, base_tokenizer = ml_engine.get_base_model()
        device = ml_engine.device

        for item in parsed_items:
            original_text = item.get('text', '') 
            res_type = item.get('type', 'GENERAL') # 기본값 설정으로 안정성 확보

            if not original_text: continue # 빈 문장 건너뛰기

            # [STEP 3] 유형별 분기 처리
            if res_type == "GENERAL":
                # 답변 전용 LLM 함수 호출 (DB 검색 생략으로 속도 향상)
                answer_data = await self._get_simple_answer(original_text)
                # --- [CASE A] 단순 질문 처리 ---
                analysis_results.append({
                "clause": original_text,
                "result_type": "GENERAL",
                "level": "SAFE",
                "score": 0.0,
                "reason": "일반 법률 문의 답변",
                "proposed_text": answer_data.get("answer", ""), # 답변 내용
                "tags": ["#일반문의"],
                "legal_basis": [],
                "precedents": []
                })
            
            else:
                # --- [CASE B] 조항 분석 처리 ---
                
                # 1. KoELECTRA 위험 탐지
                inputs = small_tokenizer(original_text, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
                with torch.no_grad():
                    probs = F.softmax(small_model(**inputs).logits, dim=-1)
                    confidence = probs[0][1].item() * 100
                all_scores.append(confidence)

                # 2. Base 모델을 사용한 정밀 리랭킹 (Re-ranking)
                refined_laws_obj = None
                refined_precedents_obj = None

                # 위험도가 어느 정도 있을 때만 리랭킹 수행 (효율성)
                if confidence >= 20:
                    
                    raw_laws, raw_precedents = self.db_search.get_related_data(original_text, top_k=10)
                    # 법령 리랭킹
                    if raw_laws:
                        law_scores = []
                        seen_laws = set()
                        for law in raw_laws:
                            if law.keyword in seen_laws: continue
                            law_inputs = base_tokenizer(original_text, law.summary, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
                            with torch.no_grad():
                                law_probs = F.softmax(base_model(**law_inputs).logits, dim=-1)
                                law_scores.append((law_probs[0][1].item(), law))
                                seen_laws.add(law.keyword)
                        law_scores.sort(key=lambda x: x[0], reverse=True)
                        refined_laws_obj = law_scores[0][1] if law_scores else None

                    # 판례 리랭킹
                    if raw_precedents:
                        pre_scores = []
                        seen_pre = set()
                        for pre in raw_precedents:
                            if pre.case_number in seen_pre: continue
                            pre_inputs = base_tokenizer(original_text, pre.content, return_tensors="pt", truncation=True, max_length=settings.MAX_SEQ_LENGTH, padding=True).to(device)
                            with torch.no_grad():
                                pre_probs = F.softmax(base_model(**pre_inputs).logits, dim=-1)
                                pre_scores.append((pre_probs[0][1].item(), pre))
                                seen_pre.add(pre.case_number)
                        pre_scores.sort(key=lambda x: x[0], reverse=True)
                        refined_precedents_obj = pre_scores[0][1] if pre_scores else None
                        
                # 3. 리랭킹된 결과를 바탕으로 최종 LLM 분석 리포트 갱신 
                final_report = await self._generate_legal_report(
                    clause=original_text,
                    law=refined_laws_obj,        # 리랭킹으로 찾은 최적의 법령
                    precedent=refined_precedents_obj  # 리랭킹으로 찾은 최적의 판례
                )
                level = "EXTREME" if confidence >= 80 else "DANGER" if confidence >= 60 else \
                        "WARNING" if confidence >= 40 else "CAUTION" if confidence >= 20 else "SAFE"

                analysis_results.append({
                    "clause": original_text,
                    "result_type": "ANALYSIS",
                    "level": level,
                    "score": round(confidence, 2),
                    "reason": final_report.get("reason", "조항 분석 완료"),
                    "proposed_text": final_report.get("proposed_text", ""),
                    "tags": ["#부당계약", "#검토필요"] if level != "SAFE" else ["#안전", "#준수"],
                    "legal_basis": final_report.get("legal_basis", []),
                    "precedents": final_report.get("precedents", [])
                })

        return {
            "status": "success",
            "doc_name": doc_name,
            "results": analysis_results,
            "total_risk_score": round(sum(all_scores) / len(all_scores), 2) if all_scores else 0,
            "analyzed_at": now
        }

    async def analyze_pdf(self, file_content: bytes, filename: str):
        full_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"
        refined_text = self.processor.clean_pdf_text(full_text)
        return await self.analyze(refined_text, filename, "file")