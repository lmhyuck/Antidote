import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__)) # app/core
app_dir = os.path.dirname(current_dir) # app
env_path = os.path.join(app_dir, ".env") # 루트의 .env 참조

class Settings(BaseSettings):
    # [1] Project Basic Config
    PROJECT_NAME: str = "Antidote"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # [2] Database Config
    DATABASE_URL: str

# [3] AI Model Names
    KOELECTRA_BASE_MODEL: str = "monologg/koelectra-base-v3-discriminator"
    KOELECTRA_SMALL_MODEL: str = "monologg/koelectra-small-v3-discriminator"
    BGE_M3_MODEL: str = "BAAI/bge-m3"

    # [4] Vector Dimensions
    # LegalKnowledge, LaborLaw 테이블용 (bge-m3)
    BGE_M3_DIMENSION: int = 1024
    
    # ContractAnalysis 테이블의 cls_vector 저장용
    # 어떤 모델의 CLS를 저장하느냐에 따라 선택해서 사용
    KOELECTRA_BASE_DIMENSION: int = 768
    KOELECTRA_SMALL_DIMENSION: int = 512 

    # 파이프라인에서 기본으로 사용할 차원 지정 (하위 호환성)
    VECTOR_DIMENSION: int = 1024

    # [6] External API Keys
    OPENAI_API_KEY: Optional[str] = None
    OCR_API_URL: Optional[str] = None
    OCR_SECRET_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )

settings = Settings()