# OCR 및 비식별화
import requests
import uuid
import time
import json
import logging
from app.core.config import settings

from typing import Optional

logger = logging.getLogger(__name__)

class OCRHandler:
    def __init__(self):
        self.api_url = settings.OCR_API_URL 
        self.secret_key = settings.OCR_SECRET_KEY
    
    # Mock(가짜 데이터) 테스트용 처리 로직
    def extract_text(self, file_content: bytes, file_name: str) -> Optional[str]:
        """
        OCR 추출 로직 (실제 API 미연결 시 Mock 데이터 반환)
        """
        # 1. Mock 모드 판별 (URL이 가짜거나 키가 없는 경우)
        is_mock_mode = "your-clova" in self.api_url or not self.secret_key or self.secret_key == "your_secret_key"

        if is_mock_mode:
            logger.info(f"🛠️ [Mock Mode] '{file_name}' 분석 시뮬레이션 중...")
            
            # 실제 네트워크 통신을 하는 것처럼 1.5초 정도 대기 (UX 테스트용)
            time.sleep(1.5) 
            
            # 테스트용 더미 텍스트 (실제 근로계약서 양식과 유사하게 구성)
            mock_response = (
                "표준 근로계약서\n\n"
                "1. 근로계약기간 : 2026년 5월 1일부터 2027년 4월 30일까지\n"
                "2. 근무장소 : 서울특별시 강남구 테헤란로 123 (주)안티도트 본사\n"
                "3. 업무내용 : 백엔드 및 데이터 엔지니어링 운영\n"
                "4. 소정근로시간 : 09시 00분부터 18시 00분까지 (휴게시간 : 12시~13시)\n"
                "5. 근무일/휴일 : 매주 5일(월~금) 근무, 주휴일 매주 일요일\n"
                "6. 임금 : 월급 4,000,000원 (기본급 기준)\n"
                "7. 기타 : 본 계약에 정함이 없는 사항은 근로기준법에 따름."
            )
            return mock_response

        # 2. 실제 API 호출 로직 (생략)
        try:
            # 여기에 기존 requests 호출 로직 작성
            pass
        except Exception as e:
            logger.error(f"OCR 실행 중 오류 발생: {e}")
            return None
        
    # 실제 처리 로직
    # def extract_text(self, file_content: bytes, file_name: str):
    #     """
    #     파일의 바이너리 데이터를 받아 OCR을 수행하고 텍스트만 반환합니다.
    #     """
    #     request_json = {
    #         'images': [
    #             {
    #                 'format': file_name.split('.')[-1],
    #                 'name': 'contract_page'
    #             }
    #         ],
    #         'requestId': str(uuid.uuid4()),
    #         'version': 'V2',
    #         'timestamp': int(round(time.time() * 1000))
    #     }

    #     payload = {'message': json.dumps(request_json).encode('UTF-8')}
    #     files = [('file', file_content)]
    #     headers = {'X-OCR-SECRET': self.secret_key}

    #     try:
    #         response = requests.post(self.api_url, headers=headers, data=payload, files=files)
    #         response.raise_for_status()
    #         result = response.json()
            
    #         # 인식된 텍스트들을 하나의 문자열로 합침
    #         full_text = ""
    #         for image in result.get('images', []):
    #             for field in image.get('fields', []):
    #                 full_text += field.get('inferText', '') + " "
            
    #         return self._preprocess_text(full_text)
            
    #     except Exception as e:
    #         print(f"OCR Error: {e}")
    #         return None

    def _preprocess_text(self, text: str):
        """
        OCR 결과물에서 불필요한 공백이나 특수문자를 정제합니다.
        """
        # 1. 여러 개의 공백을 하나로 축소
        text = " ".join(text.split())
        # 2. 분석에 방해되는 특수문자 제거 (필요에 따라 조절)
        # text = re.sub(r'[^\w\s\d.()]', '', text) 
        return text.strip()

ocr_manager = OCRHandler()