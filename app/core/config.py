# .env 로드 및 전역 설정

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__)) # app/core
app_dir = os.path.dirname(current_dir) # app
env_path = os.path.join(app_dir, ".env")

class Settings(BaseSettings):
    # [1] Project Basic Config
    PROJECT_NAME: str = "Antidote"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # [2] Database Config (PostgreSQL/PostGIS)
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/antidote"

    # [3] AI Model Config (koELECTRA)
    MODEL_NAME: str = "monologg/koelectra-base-v3-discriminator"
    MAX_SEQ_LENGTH: int = 512
    VECTOR_DIMENSION: int = 768

    # [4] OCR Config (Naver CLOVA OCR)
    # 실제 키가 없을 때 에러가 나지 않도록 기본값을 주거나 Optional로 설정합니다.
    OCR_API_URL: str = "https://your-ocr-endpoint.com"
    OCR_SECRET_KEY: str = "your-secret-key"

    # [5] External API Config
    # OpenAI 키가 없으면 ValidationError가 발생하므로 Optional로 처리합니다.
    OPENAI_API_KEY: Optional[str] = None

    # [6] Pydantic Settings Configuration
    # .env 파일을 찾아서 환경변수로 로드합니다.
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,  # 대소문자 구분 없이 .env 키값 매칭
        extra='ignore'
    )

# 전역 객체 생성
settings = Settings()