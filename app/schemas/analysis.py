from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TextInput(BaseModel):
    content: str
    doc_name: Optional[str] = "Direct Input"

class LegalBasis(BaseModel):
    title: str
    summary: str

class PrecedentDetail(BaseModel):
    title: str
    content: str

# --- 수정 및 추가된 부분 ---
class ResultDetail(BaseModel):
    clause: str
    level: str            
    score: float
    # 개별 렌더링을 위한 필드 추가
    reason: str = ""       # 판단 근거
    proposed_text: str = "" # 수정 제안 문구
    legal_basis: List[LegalBasis] = []
    precedents: List[PrecedentDetail] = []
    tags: List[str] = []

class AnalysisReport(BaseModel):
    status: str 
    message: str 
    doc_name: str
    total_risk_score: float
    results: List[ResultDetail]
    analyzed_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))