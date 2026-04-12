import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class ContractSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        # chunk_size: 한 조각의 최대 길이
        # chunk_overlap: 문맥 유지를 위해 앞 조각과 겹치는 부분 (중요!)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""] # 계약서는 줄바꿈 기준이 가장 깔끔함
        )

    def split_contract(self, text: str) -> List[str]:
        if not text:
            return []
        
        chunks = self.splitter.split_text(text)
        logger.info(f"✂️ 텍스트 분할 완료: {len(chunks)} 개의 청크 생성")
        return chunks

contract_splitter = ContractSplitter()