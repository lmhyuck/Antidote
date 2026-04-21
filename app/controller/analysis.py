from fastapi import UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

# 분리된 서비스와 스키마 임포트
from app.services.analyzer import LegalAnalyzer  # 파일명에 맞춰 수정
from app.schemas.analysis import TextInput, AnalysisReport

# 로깅 설정
logger = logging.getLogger("uvicorn.error")

# 서비스 인스턴스 생성
analyzer = LegalAnalyzer()

async def contract(file: UploadFile = File(...)):
    """PDF 파일 업로드 분석 컨트롤러"""
    try:
        logger.info(f"📥 파일 수신: {file.filename} ({file.content_type})")
        
        # 1. 파일 확장자 검증
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDF 파일만 업로드 가능합니다."
            )

        # 2. 파일 내용 읽기
        content = await file.read()
        
        # [보안] 파일 크기 체크 (예: 10MB 제한)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="파일 크기가 너무 큽니다 (최대 10MB)."
            )
        
        # 3. 서비스 호출 (LegalAnalyzer의 메서드 호출)
        # 분리된 구조에 따라 analyze_pdf 호출
        report_data = analyzer.analyze_pdf(content, file.filename)
        
        # 4. 결과 반환
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(report_data)
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"❌ PDF 컨트롤러 오류: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "서버 내부 분석 오류", "error": str(e)}
        )
    finally:
        await file.close()

async def analyze_text(data: TextInput):
    """직접 입력 텍스트 분석 컨트롤러"""
    try:
        logger.info(f"📝 텍스트 분석 요청 수신: {data.doc_name}")
        
        # 서비스 호출 (LegalAnalyzer의 analyze 메서드 활용)
        report_data = analyzer.analyze(data.content, data.doc_name)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(report_data)
        )
    except Exception as e:
        logger.error(f"❌ 텍스트 분석 컨트롤러 오류: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "텍스트 분석 중 오류 발생", "error": str(e)}
        )