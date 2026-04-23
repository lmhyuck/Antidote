import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from google import genai


class ModelLoader:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.genai_client = None
        self.model_name = settings.GEMINI_MODEL_NAME 

        print("==================================================")
        print("⏳ Antidote AI Engines Loading... (Device: cpu)")
        
        try:
            self.genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            print(f"✅ Gemini 3.1 SDK Ready: {self.model_name}")
        except Exception as e:
            print(f"❌ Gemini Setup Failed: {e}")
            
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

        print("✅ All Models Loaded Successfully!")
        print(f"   - Small  : {self.small_model_name}")
        print(f"   - Base   : {self.base_model_name}")
        print(f"   - BGE-M3 : {self.bge_model_name}")
        print("==================================================")

    def get_gemini_client(self):
        return self.genai_client, self.model_name

    def get_small_model(self):
        return self.small_model, self.small_tokenizer

    def get_base_model(self):
        return self.base_model, self.base_tokenizer

    def get_bge_model(self):
        return self.bge_model
    

# 싱글톤 객체 생성
ml_engine = ModelLoader()