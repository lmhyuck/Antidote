import fitz
import torch
import logging
import torch.nn.functional as F
from datetime import datetime
from app.core.model_loader import ml_engine
from .text_processor import TextProcessor
from .db_search import DBSearch
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")

class LegalAnalyzer:
    def __init__(self):
        self.processor = TextProcessor()
        self.db_search = DBSearch()

    def analyze(self, text: str, doc_name: str):
        # 1. 텍스트 청킹
        chunks = self.processor.smart_chunking(text)
        analysis_results = [] # 모든 조항의 결과를 담을 리스트
        all_scores = []
        
        # 모델 및 디바이스 설정
        small_model, small_tokenizer = ml_engine.get_small_model()
        base_model, base_tokenizer = ml_engine.get_base_model()
        device = ml_engine.device

        for item in chunks:
            original = item['original']
            embedding_text = item['for_embedding']

            # 2. KoELECTRA-Small 추론 (위험 탐지)
            inputs = small_tokenizer(original, return_tensors="pt", truncation=True, max_length=512, padding=True).to(device)

            with torch.no_grad():
                outputs = small_model(**inputs)
                probs = F.softmax(outputs.logits, dim=-1)
                confidence = probs[0][1].item() * 100
            
            all_scores.append(confidence)

            # 3. 판별 로직 (40점 기준 분기)
            if confidence >= 40:
                # [위험/주의] 벡터 DB에서 관련 법령 및 판례 검색 (1차 후보군 10개 추출)
                raw_laws, raw_precedents = self.db_search.get_related_data(embedding_text, top_k=10)
                
                # --- [추가] KoELECTRA-Base를 이용한 2차 정밀 검증 (Re-ranking) ---
                refined_laws = []
                if raw_laws:
                    law_scores = []
                    for law in raw_laws:
                        # 조항과 법령을 결합하여 교차 인코딩 (Cross-Encoding)
                        law_inputs = base_tokenizer(
                            original, law.summary, 
                            return_tensors="pt", truncation=True, 
                            max_length=settings.MAX_SEQ_LENGTH, padding=True
                        ).to(device)
                        
                        with torch.no_grad():
                            law_outputs = base_model(**law_inputs)
                            law_probs = F.softmax(law_outputs.logits, dim=-1)
                            # 관련성 점수 추출 (Positive 확률)
                            rel_score = law_probs[0][1].item()
                            law_scores.append((rel_score, law))
                    # 점수 순으로 정렬 후 상위 2개만 추출
                    law_scores.sort(key=lambda x: x[0], reverse=True)
                    refined_laws = [item[1] for item in law_scores[:2]]

                refined_precedents = []
                if raw_precedents:
                    pre_scores = []
                    for pre in raw_precedents:
                        pre_inputs = base_tokenizer(
                            original, pre.content, 
                            return_tensors="pt", truncation=True, 
                            max_length=settings.MAX_SEQ_LENGTH, padding=True
                        ).to(device)
                        
                        with torch.no_grad():
                            pre_outputs = base_model(**pre_inputs)
                            pre_probs = F.softmax(pre_outputs.logits, dim=-1)
                            rel_score = pre_probs[0][1].item()
                            pre_scores.append((rel_score, pre))
                    # 점수 순으로 정렬 후 상위 2개만 추출
                    pre_scores.sort(key=lambda x: x[0], reverse=True)
                    refined_precedents = [item[1] for item in pre_scores[:2]]
                # -----------------------------------------------------------

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
                # [안전] 40점 미만 조항
                analysis_results.append({
                    "clause": original,
                    "level": "SAFE",
                    "score": round(confidence, 2),
                    "description": "해당 조항은 표준 근로계약 기준에 부합하며, 특별한 위험 요소가 발견되지 않았습니다.",
                    "tags": ["#안전", "#표준준수"],
                    "legal_basis": [],
                    "precedents": []
                })

        # 4. 전체 위험도 산술 평균 산출 로직
        if all_scores:
            total_avg_score = sum(all_scores) / len(all_scores)
            total_risk_score = round(total_avg_score, 2)
            
        else:
            total_risk_score = 0

        return {
            "doc_name": doc_name,
            "total_risk_score": total_risk_score,
            "results": analysis_results, 
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def analyze_pdf(self, file_content: bytes, filename: str):
        full_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"

        refined_text = self.processor.clean_pdf_text(full_text)
        return self.analyze(refined_text, filename)