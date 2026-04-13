import os
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.services.pdf_extractor import pdf_extractor
from app.services.text_splitter import contract_splitter
from app.core.model_loader import ml_engine  # bge-m3 모델 사용
from app.db.vector_db import SessionLocal
from app.db.vector_db import LaborLaw  # DB 모델

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("uvicorn.error")

def get_related_laws(query_text: str, top_k: int = 3):
    """
    청크된 계약서 조항과 가장 유사한 근로기준법 조항을 DB에서 찾아옵니다.
    """
    db: Session = SessionLocal()
    try:
        # 1. 쿼리 텍스트(계약서 조항) 벡터화
        model = ml_engine.get_bge_model()
        query_embedding = model.encode(query_text).tolist()

        # 2. 벡터 유사도 검색 (Cosine Similarity)
        # embedding 컬럼과 query_embedding 사이의 거리를 계산하여 가까운 순으로 가져옴
        related_laws = db.query(LaborLaw).order_by(
            LaborLaw.embedding.cosine_distance(query_embedding)
        ).limit(top_k).all()

        return related_laws
    except Exception as e:
        logger.error(f"❌ 유사 법령 검색 중 오류: {e}")
        return []
    finally:
        db.close()

def test_ocr_and_search_flow():
    """OCR -> 분할 -> 유사 법령 검색까지의 흐름을 테스트합니다."""
    
    # 1. 파일 경로 설정
    base_dir = os.getcwd()
    sample_path = os.path.join(base_dir, "app", "data", "samples", "근로계약서_샘플.pdf")
    
    if not os.path.exists(sample_path):
        logger.error(f"❌ 파일을 찾을 수 없습니다: {sample_path}")
        return

    try:
        # 2. OCR 추출
        logger.info("--- [STEP 1] OCR 추출 시작 ---")
        with open(sample_path, "rb") as f:
            file_content = f.read()
            file_name = os.path.basename(sample_path)
        
        raw_text: Optional[str] = pdf_extractor.extract_text(file_content, file_name)
        if not raw_text: return

        # 3. 텍스트 분할 (Chunking)
        logger.info("--- [STEP 2] 텍스트 분할 시작 ---")
        chunks: List[str] = contract_splitter.split_contract(raw_text)
        
        # 4. 각 청크별 유사 법령 매칭 테스트
        logger.info("--- [STEP 3] 조항별 관련 근로기준법 매칭 시작 ---")
        
        print("\n" + "="*80)
        print(f"🚀 통합 테스트 결과: 총 {len(chunks)}개 조항 분석")
        print("="*80)

        for i, chunk in enumerate(chunks, 1):
            print(f"\n🔍 [계약서 조항 {i}]")
            print(f"내용: {chunk.strip()[:100]}...") # 너무 길면 잘라서 출력
            
            # DB에서 관련 법령 찾아오기
            related_laws = get_related_laws(chunk)
            
            if related_laws:
                print(f"💡 관련 근로기준법 근거:")
                for law in related_laws:
                    # law.embedding은 너무 길어서 출력에서 제외
                    print(f"   - {law.full_reference}")
                    print(f"     내용: {law.law_content[:150]}...")
            else:
                print("   - ⚠️ 관련된 법령을 찾을 수 없습니다.")
            print("-" * 60)

    except Exception as e:
        logger.error(f"❌ 통합 테스트 중 에러 발생: {e}", exc_info=True)

if __name__ == "__main__":
    test_ocr_and_search_flow()