import os
import logging
from typing import List, Optional
from app.services.ocr_handler import ocr_manager
from app.services.text_splitter import contract_splitter

# 로깅 설정 (운영 환경 수준)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_ocr_flow():
    """OCR 추출부터 텍스트 분할까지의 전체 프로세스를 테스트합니다."""
    
    # 1. 파일 경로 설정 (기존 확인된 경로)
    base_dir = os.getcwd()
    sample_path = os.path.join(base_dir, "app", "data", "samples", "근로계약서_샘플.pdf")
    
    if not os.path.exists(sample_path):
        logger.error(f"❌ 파일을 찾을 수 없습니다: {sample_path}")
        return

    try:
        # 2. PDF 로드 및 OCR 추출
        logger.info("--- [STEP 1] OCR 추출 시작 ---")
        with open(sample_path, "rb") as f:
            file_content = f.read()
            file_name = os.path.basename(sample_path)
        
        raw_text: Optional[str] = ocr_manager.extract_text(file_content, file_name)
        
        if not raw_text:
            logger.error("❌ OCR 결과가 없습니다.")
            return

        # 3. 텍스트 분할 (Splitter)
        logger.info("--- [STEP 2] 텍스트 분할(Chunking) 시작 ---")
        chunks: List[str] = contract_splitter.split_contract(raw_text)
        
        # 4. 최종 결과 출력
        print("\n" + "🚀" * 30)
        logger.info(f"통합 프로세스 완료! 총 {len(chunks)}개의 청크가 생성되었습니다.")
        print("🚀" * 30)

        for i, chunk in enumerate(chunks, 1):
            print(f"\n[Chunk {i}] ({len(chunk)} characters)")
            print("-" * 40)
            print(chunk.strip())
            print("-" * 40)

    except Exception as e:
        logger.error(f"❌ 통합 테스트 중 에러 발생: {e}", exc_info=True)

if __name__ == "__main__":
    test_ocr_flow()