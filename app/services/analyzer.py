import fitz
import torch
import logging
from datetime import datetime
from app.core.model_loader import ml_engine
from .text_processor import TextProcessor
from .db_search import DBSearch

logger = logging.getLogger("uvicorn.error")

class LegalAnalyzer:
    def __init__(self):
        self.processor = TextProcessor()
        self.db_search = DBSearch()

    def analyze(self, text: str, doc_name: str):
        # 1. 텍스트 청킹
        chunks = self.processor.smart_chunking(text)
        detected_risks = []
        all_scores = []
        
        model = ml_engine.small_model
        tokenizer = ml_engine.small_tokenizer
        device = ml_engine.device

        for item in chunks:
            original = item['original']
            embedding_text = item['for_embedding']

            # 2. KoELECTRA 추론
            inputs = tokenizer(original, return_tensors="pt", truncation=True, max_length=512, padding=True).to(device)

            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                confidence = probs[0][1].item() * 100
            all_scores.append(confidence)

            # 3. 위험 조항 판별 및 데이터 보강 (Threshold: 40)
            if confidence >= 40:
                # 벡터 DB에서 관련 법령 및 판례 검색
                laws, precedents = self.db_search.get_related_data(embedding_text)
                
                detected_risks.append({
                    "clause": original,
                    "level": "DANGER" if confidence >= 70 else "WARNING",
                    "score": round(confidence, 2),
                    "description": f"해당 조항은 {laws[0].keyword if laws else '법령'} 위반 소지가 있습니다.",
                    "tags": ["#부속계약", "#검토필요"],
                    "legal_basis": [{"title": l.keyword, "summary": l.summary} for l in laws],
                    "precedents": [{"title": p.case_number, "content": p.content} for p in precedents]
                })

        # 4. 전체 위험도 산출 로직 개선 (희석 방지)
        if all_scores:
            # 산술 평균은 정상 조항에 의해 위험도가 묻히므로, 
            # 가장 높은 위험도(Max)와 주의군 이상의 평균을 조합하여 산출합니다.
            max_score = max(all_scores)
            risky_elements = [s for s in all_scores if s >= 40]
            avg_risky = sum(risky_elements) / len(risky_elements) if risky_elements else sum(all_scores)/len(all_scores)
            
            # 최댓값에 70% 비중을 두어 독소 조항의 존재감을 부각
            total_risk_score = round((max_score * 0.7) + (avg_risky * 0.3), 2)
        else:
            total_risk_score = 0

        return {
            "doc_name": doc_name,
            "total_risk_score": total_risk_score,
            "risks": detected_risks,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def analyze_pdf(self, file_content: bytes, filename: str):
        full_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                # 우선 raw 텍스트를 다 긁어모읍니다.
                full_text += page.get_text("text") + "\n"

        # [수정] 이미 만들어둔 메소드를 여기서 딱 한 번 호출!
        # 여기서 "6.임금" 같은 게 다 잘리고 문자열로 예쁘게 변환됩니다.
        refined_text = self.processor.clean_pdf_text(full_text)

        # 정제된 텍스트를 기존 analyze 로직으로 전달
        return self.analyze(refined_text, filename)