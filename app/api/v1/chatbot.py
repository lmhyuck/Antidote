#법률 챗봇 엔드포인트
from fastapi import APIRouter

router = APIRouter()

@router.post("/ask")
async def ask_legal_question(question: str):
    """
    [UI-03] 법률 질의응답 (껍데기)
    """
    return {"answer": f"'{question}'에 대한 답변을 준비 중입니다. 판례 DB를 검색하고 있습니다.", "status": "waiting"}