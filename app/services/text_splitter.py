import re
import logging
from typing import List

logger = logging.getLogger(__name__)

class ContractSplitter:
    def __init__(self):
        # 조항을 구분할 정규표현식 패턴 (숫자. 형태)
        # 예: "1. ", "2. " 등을 기준으로 분할
        self.split_pattern = re.compile(r'\n(?=\d+\.)')

    def split_contract(self, text: str) -> List[str]:
        if not text:
            return []

        # 1. 정규표현식 패턴을 기준으로 텍스트 분할
        # 단순 split이 아니라 패턴을 유지하면서 자르기 위해 re.split 사용
        chunks = self.split_pattern.split(text)

        # 2. 공백 제거 및 빈 청크 필터링
        cleaned_chunks = [c.strip() for c in chunks if c.strip()]

        logger.info(f"✂️ 조항 기준 분할 완료: {len(cleaned_chunks)} 개의 조항 생성")
        return cleaned_chunks

contract_splitter = ContractSplitter()