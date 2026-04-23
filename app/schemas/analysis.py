from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TextInput(BaseModel):
    content: str
    doc_name: Optional[str] = "Direct Input"

# 법령 상세 정보
class LegalBasis(BaseModel):
    title: str
    summary: str

# 판례 상세 정보
class PrecedentDetail(BaseModel):
    title: str
    content: str

# 결과 항목 상세 (서비스 로직과 1:1 매칭)
class ResultDetail(BaseModel):
    clause: str
    level: str  # DANGER, WARNING, SAFE
    score: float
    description: str
    tags: List[str] = []
    legal_basis: List[LegalBasis] = []
    precedents: List[PrecedentDetail] = []

# 최종 응답 리포트
class AnalysisReport(BaseModel):
    status: str # "success" 또는 "invalid_query"
    message: str # 성공 시 "분석 완료", 실패 시 가이드 메시지
    doc_name: str
    total_risk_score: float
    results: List[ResultDetail]
    analyzed_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))