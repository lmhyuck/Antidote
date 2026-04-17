from sqlalchemy import Column, Integer, Text, String, Float, DateTime, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector
from datetime import datetime
import logging

from app.core.config import settings

# 로깅 설정
logger = logging.getLogger(__name__)

Base = declarative_base()

# 1. 실제 판례 데이터 테이블 (Case Law)
class Precedent(Base):
    """
    사건번호, 위반조항을 기반으로 판례 내용을 벡터화하여 저장
    """
    __tablename__ = 'precedents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_number = Column(String, unique=True, index=True, nullable=False) # 사건번호
    violated_article = Column(String, index=True)                       # 위반조항 (예: 근로기준법 제43조)
    content = Column(Text, nullable=False)                             # 판례 내용 원문
    embedding = Column(Vector(settings.BGE_M3_DIMENSION), nullable=False) # bge-m3 벡터
    
    created_at = Column(DateTime, default=datetime.utcnow)

# 2. 근로기준법 데이터 테이블 (Statutes)
class LaborLaw(Base):
    """
    수정된 CSV 구조를 반영한 근로기준법 데이터 테이블
    """
    __tablename__ = 'labor_laws'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 1. 고유 식별 정보 (검색 및 필터링용)
    article_num = Column(String, index=True)   # 조 번호 (제1조)
    paragraph_num = Column(String, index=True) # 조항 번호 (제1조 1항 등)
    keyword = Column(String, index=True)       # 조(키워드) (제1조(목적) 등)
    
    # 2. 내용 정보 (검색 및 응답용)
    summary = Column(Text, nullable=True)      # 추천 요약 (LLM에게 제공할 핵심 요약)
    law_content = Column(Text, nullable=False) # 통합 내용 (원문 전체)
    
    # 4. 벡터화 정보 (BGE-M3)
    embedding = Column(Vector(settings.BGE_M3_DIMENSION), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

# 3. 계약서 조항 분석 결과 테이블 (Analysis Results)
class ContractAnalysis(Base):
    """
    분석된 독소 조항, 신뢰도, 결과, 수정본을 저장
    """
    __tablename__ = 'contract_analysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(String, index=True, nullable=False)
    original_clause = Column(Text, nullable=False)     # 분석 대상 원문 조항
    
    prediction_result = Column(String)                # 독소 조항 여부 (Toxic/Safe)
    confidence_score = Column(Float)                  # 모델 신뢰도
    analysis_report = Column(Text)                    # 상세 분석 내용
    suggested_revision = Column(Text)                 # AI가 제안한 수정본
    
    created_at = Column(DateTime, default=datetime.utcnow)

# --- DB 엔진 및 초기화 ---
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """DB 초기화 및 벡터 인덱스 최적화"""
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            Base.metadata.create_all(bind=engine)
            
            # HNSW 인덱스: 판례와 법령 검색 속도 향상
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_precedents_v ON precedents USING hnsw (embedding vector_cosine_ops);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_labor_laws_v ON labor_laws USING hnsw (embedding vector_cosine_ops);"))
            conn.commit()
            
        logger.info("✅ Antidote 3-Tier DB Schema 구축 완료")
    except SQLAlchemyError as e:
        logger.error(f"❌ DB 초기화 실패: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()