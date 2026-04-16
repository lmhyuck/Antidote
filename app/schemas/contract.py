from pydantic import BaseModel
from typing import List

# 분석 결과 확인을 위한 리포트 규격
class LegalReport(BaseModel):
    title: str                         # 리포트 제목 (파일명 등)
    risk_score: int                    # 위험도 점수 (0~100)
    detected_risks: List[str]          # 감지된 주요 리스크 항목들
    improvement_suggestions: List[str] # 개선 제안 사항
    analyzed_at: str                   # 분석 일시