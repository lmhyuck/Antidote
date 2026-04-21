from fastapi import APIRouter
from app.controller import analysis

router = APIRouter(prefix="/analysis", tags=["Legal Analysis"])

# [Case A] PDF 파일 업로드 분석
router.add_api_route("/contract", analysis.contract, methods=["POST"])

# [Case B] 사용자 직접 입력 텍스트 분석
router.add_api_route("/text", analysis.analyze_text, methods=["POST"])