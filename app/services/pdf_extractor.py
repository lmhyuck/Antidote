import fitz  # PyMuPDF
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PDFTextExtractor:
    def __init__(self):
        pass

    def extract_text(self, file_content: bytes, file_name: str = "Unknown") -> Optional[str]:
        """
        PDF 바이너리에서 텍스트를 직접 추출합니다.
        """
        try:
            logger.info(f"📄 [PDF Direct Extraction] '{file_name}' 분석 시작...")
            
            # 메모리 내의 바이트 데이터를 PDF 문서로 로드
            doc = fitz.open(stream=file_content, filetype="pdf")
            full_text = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # 텍스트 추출
                text = page.get_text("text")
                if text.strip():
                    full_text.append(text)

            doc.close()
            
            if not full_text:
                logger.warning(f"⚠️ '{file_name}': 추출 가능한 텍스트가 없습니다. (이미지 기반 PDF일 가능성)")
                return None

            return "\n".join(full_text)

        except Exception as e:
            logger.error(f"❌ '{file_name}' PDF 추출 중 에러 발생: {str(e)}")
            return None

# 인스턴스 생성
pdf_extractor = PDFTextExtractor()