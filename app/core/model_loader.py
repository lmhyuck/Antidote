# 모델 로더 및 환경 세팅
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import settings

class ModelLoader:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = settings.MODEL_NAME
        
        # 1. 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # 2. 분류 모델 로드 (유/불리 2개 라벨 기준)
        # num_labels는 나중에 학습된 가중치를 불러올 때 중요합니다.
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, 
            num_labels=2 
        ).to(self.device)
        
        print(f"✅ 모델 로드 완료: {self.model_name} (Device: {self.device})")

# 전역 객체로 생성하여 어디서든 참조 가능하게 함
ml_engine = ModelLoader()