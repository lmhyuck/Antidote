from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import analysis, chatbot
from app.core.config import settings
from app.db.vector_db import engine, Base
from app.db.vector_db import init_db
from app.core.model_loader import ml_engine

# 1. 데이터베이스 테이블 생성 (애플리케이션 실행 시)
init_db()

# koELECTRA 모델 메모리 로드
# 이 시점에 ml_engine 객체가 생성되면서 모델을 메모리에 올립니다.
_ = ml_engine.model

# pgvector 확장이 활성화된 DB에서 AntidoteCase 테이블을 생성합니다.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="근로계약서 독소조항 분석 및 법률 질의응답 서비스 'Antidote'",
    version="1.0.0"
)

# 2. CORS 설정 (프론트엔드 격리 대응)
# 프론트엔드와 백엔드가 포트가 다르므로 통신 허용이 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 프론트엔드 주소만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. API 라우터 등록
# 각 기능을 별도 파일로 분리하여 유지보수성을 높였습니다.
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(chatbot.router, prefix="/api/v1/chatbot", tags=["Chatbot"])

@app.get("/")
def read_root():
    """
    서버 상태 확인을 위한 헬스체크 엔드포인트
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    # 로컬 터미널에서 실행하기 위한 설정
    # 포트 넘버는 8000을 사용합니다.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)