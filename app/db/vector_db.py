from sqlalchemy import Column, Integer, Text, String, Float, DateTime, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.config import settings

Base = declarative_base()

# 1. 법률 지식 베이스 (RAG용: 판례, 법령 등)
class LegalKnowledge(Base):
    __tablename__ = 'legal_knowledge'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(settings.VECTOR_DIMENSION)) # 768차원
    reference_id = Column(String, unique=True)            # 판례 번호 등
    category = Column(String)                             # 임금, 근로시간 등
    created_at = Column(DateTime, default=datetime.utcnow)

# 2. 계약서 조항 분석 결과 (koELECTRA 추론 결과 저장용)
class ClauseAnalysis(Base):
    __tablename__ = 'clause_analyses'

    id = Column(Integer, primary_key=True)
    contract_id = Column(String, index=True)      # 계약서 식별자
    clause_text = Column(Text, nullable=False)    # 조항 원문
    
    # koELECTRA 추론 데이터
    prediction_label = Column(String)             # 유/불리 결과 (Advantage/Disadvantage)
    confidence_score = Column(Float)              # 모델 확신도
    
    # 재학습용 CLS 벡터 저장 (선택 사항이지만 강력 권장)
    # 추후 데이터 분포 분석이나 유사도 검색에 활용
    cls_vector = Column(Vector(settings.VECTOR_DIMENSION)) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

# --- DB 엔진 및 초기화 로직 ---
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """DB 초기 설정: pgvector 활성화 및 모든 테이블 생성"""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    print("✅ Antidote 하이브리드 벡터 DB 환경 구축 완료")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()