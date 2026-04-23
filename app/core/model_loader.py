import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from app.core.config import settings


class ModelLoader:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        print("==================================================")
        print(f"⏳ Antidote AI Engines Loading... (Device: {self.device})")
        
        # self.guardrail_model = None # 초기화
        # try:
        #     # hasattr로 속성이 존재하는지 먼저 체크 (안전 장치)
        #     if hasattr(settings, "GEMINI_API_KEY") and settings.GEMINI_API_KEY:
        #         genai.configure(api_key=settings.GEMINI_API_KEY)
        #         self.guardrail_model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        #         print(f"✅ Gemini SDK Ready: {settings.GEMINI_MODEL_NAME}")
        #     else:
        #         print("❌ GOOGLE_API_KEY가 Settings에 정의되지 않았습니다.")
        # except Exception as e:
        #     print(f"❌ Gemini Setup Failed: {e}")
            
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

    # def get_guardrail_model(self):
    #     return self.guardrail_model

    def get_small_model(self):
        return self.small_model, self.small_tokenizer

    def get_base_model(self):
        return self.base_model, self.base_tokenizer

    def get_bge_model(self):
        return self.bge_model
    

# 싱글톤 객체 생성
ml_engine = ModelLoader()