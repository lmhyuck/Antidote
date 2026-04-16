import os
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.services.extractor import extractor as ex
from app.services.text_splitter import contract_splitter
from app.core.model_loader import ml_engine
from app.db.vector_db import SessionLocal
from app.db.vector_db import LaborLaw, Precedent 

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("uvicorn.error")

def get_related_laws(query_text: str, top_k: int = 2):
    """계약서 조항과 유사한 근로기준법 조항 검색"""
    db: Session = SessionLocal()
    try:
        model = ml_engine.get_bge_model()
        query_embedding = model.encode(query_text).tolist()

        related_laws = db.query(LaborLaw).order_by(
            LaborLaw.embedding.cosine_distance(query_embedding)
        ).limit(top_k).all()

        return related_laws
    except Exception as e:
        logger.error(f"❌ 유사 법령 검색 중 오류: {e}")
        return []
    finally:
        db.close()

def get_related_precedents(query_text: str, top_k: int = 2):
    """
    [추가] 계약서 조항과 유사한 실제 판례를 DB에서 찾아옵니다.
    """
    db: Session = SessionLocal()
    try:
        model = ml_engine.get_bge_model()
        # 쿼리 임베딩 생성
        query_embedding = model.encode(query_text).tolist()

        # Precedent 테이블에서 벡터 유사도 검색
        related_precedents = db.query(Precedent).order_by(
            Precedent.embedding.cosine_distance(query_embedding)
        ).limit(top_k).all()

        return related_precedents
    except Exception as e:
        logger.error(f"❌ 유사 판례 검색 중 오류: {e}")
        return []
    finally:
        db.close()

def test_full_rag_flow():
    """OCR -> 분할 -> 법령 및 판례 검색 통합 테스트"""
    
    base_dir = os.getcwd()
    sample_path = os.path.join(base_dir, "app", "data", "samples", "근로계약서_샘플.pdf")
    
    if not os.path.exists(sample_path):
        logger.error(f"❌ 파일을 찾을 수 없습니다: {sample_path}")
        return

    try:
        # 1. OCR 추출
        logger.info("--- [STEP 1] OCR 추출 시작 ---")
        with open(sample_path, "rb") as f:
            file_content = f.read()
            file_name = os.path.basename(sample_path)
        
        raw_text: Optional[str] = ex.pdf_extractor(file_content, file_name)
        if not raw_text: return

        # 2. 텍스트 분할 (Chunking)
        logger.info("--- [STEP 2] 텍스트 분할 시작 ---")
        chunks: List[str] = contract_splitter.split_contract(raw_text)
        
        # 3. 통합 매칭 테스트
        logger.info("--- [STEP 3] 조항별 법령 및 판례 매칭 시작 ---")
        
        print("\n" + "="*80)
        print(f"🚀 Antidote RAG 통합 테스트: 총 {len(chunks)}개 조항 분석")
        print("="*80)

        for i, chunk in enumerate(chunks, 1):
            # [수정] 의미 없는 짧은 청크(공백, 줄바꿈만 있는 경우)는 건너뜁니다.
            clean_chunk = chunk.strip()
            if len(clean_chunk) < 5:  # 최소 5자 이상일 때만 분석
                continue

            print(f"\n🔍 [분석 조항 {i}]")
            print(f"내용: {clean_chunk[:100]}...") 
            
            # A. 관련 법령 검색 (변수 초기화 보장)
            related_laws = get_related_laws(clean_chunk)
            # B. 관련 판례 검색
            related_precedents = get_related_precedents(clean_chunk)
            
            # 법령 결과 출력
            print(f"\n   ⚖️ [관련 법령]")
            if related_laws:
                # 중복 출력을 방지하기 위해 집합(set) 등으로 관리할 수도 있지만, 
                # 일단 리스트 결과를 정확히 하나씩만 출력합니다.
                for law in related_laws:
                    print(f"    - {law.full_reference}")
                    print(f"      내용: {law.law_content[:100].replace(os.linesep, ' ')}...")
            else:
                print("    - ⚠️ 매칭된 법령 없음")

            # 판례 결과 출력
            print(f"\n   📜 [참조 판례]")
            if related_precedents:
                for pre in related_precedents:
                    print(f"    - 사건번호: {pre.case_number} ({pre.violated_article})")
                    print(f"      판례요약: {pre.content[:100].replace(os.linesep, ' ')}...")
            else:
                print("    - ⚠️ 매칭된 판례 없음")

            print("-" * 80)
            
            # [추가] 출력 후 명시적으로 변수 비우기 (파이썬 특성상 필수는 아니지만 안전함)
            del related_laws
            del related_precedents

    except Exception as e:
        logger.error(f"❌ 통합 테스트 중 에러 발생: {e}", exc_info=True)

if __name__ == "__main__":
    test_full_rag_flow()