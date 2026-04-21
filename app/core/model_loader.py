import torch
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from app.core.config import settings

# Uvicorn 로거와 통합하여 터미널에 로그가 반드시 찍히도록 설정
logger = logging.getLogger("uvicorn.error")

class ModelLoader:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info("==================================================")
        logger.info(f"⏳ Antidote AI Engines Loading... (Device: {self.device})")
        
        # 1. KoELECTRA-Small (Detection)
        self.small_model_name = settings.KOELECTRA_SMALL_MODEL
        self.small_tokenizer = AutoTokenizer.from_pretrained(self.small_model_name)
        self.small_model = AutoModelForSequenceClassification.from_pretrained(
            self.small_model_name
        ).to(self.device)
        # 추론 모드로 설정 (중요: 드롭아웃 등을 비활성화하여 결과 일관성 유지)
        self.small_model.eval()
        
        # 2. KoELECTRA-Base (Re-ranking)
        self.base_model_name = settings.KOELECTRA_BASE_MODEL
        self.base_tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        self.base_model = AutoModelForSequenceClassification.from_pretrained(
            self.base_model_name, num_labels=2
        ).to(self.device)

        # 3. BGE-M3 (Embedding)
        self.bge_model_name = settings.BGE_M3_MODEL
        self.bge_model = SentenceTransformer(self.bge_model_name, device=self.device)

        logger.info("✅ All Models Loaded Successfully!")
        logger.info(f"   - Small  : {self.small_model_name}")
        logger.info(f"   - Base   : {self.base_model_name}")
        logger.info(f"   - BGE-M3 : {self.bge_model_name}")
        logger.info("==================================================")

    def get_small_model(self):
        return self.small_model, self.small_tokenizer

    def get_base_model(self):
        return self.base_model, self.base_tokenizer

    def get_bge_model(self):
        return self.bge_model
    

# 싱글톤 객체 생성
ml_engine = ModelLoader()