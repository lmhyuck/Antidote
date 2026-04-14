import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import analysis, chatbot
from app.core.config import settings
from app.db.vector_db import init_db, SessionLocal,LaborLaw, Precedent

# 로깅 설정 (Uvicorn 표준 출력과 통합)
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="근로계약서 독소조항 분석 서비스 'Antidote'",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서버 시작 시 실행될 로직 (Startup Event)
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Antidote 백엔드 서비스를 시작합니다...")
    
    # 1. DB 초기화 (Table 생성 및 pgvector 확장 확인)
    try:
        init_db()
        logger.info("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")

    db = SessionLocal()
    try:
        # 2. 기초 법령 데이터(LaborLaw) 자동 적재 확인
        law_count = db.query(LaborLaw).count()
        if law_count == 0:
            logger.info("📡 기초 법령 데이터가 없습니다. 자동 벡터 적재를 시작합니다...")
            
            # store_embeddings.py (또는 ingest_laws.py)에서 인입 함수 호출
            # 순환 참조 방지를 위해 함수 내부에서 임포트
            from app.scripts.ingest_laws import ingest_labor_laws
            
            csv_path_law = "data/근로기준법_조항.csv"
            ingest_labor_laws(csv_path_law)
        else:
            logger.info(f"✅ 기존 법령 데이터 확인됨 ({law_count}건). 자동 적재를 건너뜁니다.")
            
        # 3. 실제 판례 데이터(Precedent) 자동 적재 확인
        precedent_count = db.query(Precedent).count()
        if precedent_count == 0:
            logger.info("📡 실제 판례 데이터가 없습니다. 자동 벡터 적재를 시작합니다...")
            # 순환 참조 방지를 위해 함수 내부에서 임포트
            from app.scripts.ingest_precedents import ingest_precedents
            
            # 경로 설정
            csv_path_pre = "data/실제판례.json"
            ingest_precedents(csv_path_pre)
        else:
            logger.info(f"✅ 기존 판례 데이터 확인됨 ({precedent_count}건).")
    except Exception as e:
        logger.error(f"❌ 데이터 적재 프로세스 중 오류 발생: {e}")
    finally:
        db.close()

    # 3. AI 모델 로더 상태 확인 (메모리 로드 보장)
    from app.core.model_loader import ml_engine
    logger.info(f"💡 AI 엔진 준비 상태: {ml_engine.device}")

# API 라우터 등록
app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["Analysis"])
app.include_router(chatbot.router, prefix=f"{settings.API_V1_STR}/chatbot", tags=["Chatbot"])

@app.get("/")
def health_check():
    return {
        "app": settings.PROJECT_NAME,
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    # Windows의 spawn 문제 방지를 위해 uvicorn.run 설정
    # port=8000 사용
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)