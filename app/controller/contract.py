from fastapi import UploadFile, File, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.extractor import extractor as ex
import logging

# 로깅 설정
logger = logging.getLogger("uvicorn.error")

async def contract(file: UploadFile = File(...)):
    try:
        logger.info(f"📥 파일 수신: {file.filename}, 컨텐츠 타입: {file.content_type}")
        # 1. 파일 확장자 체크
        if not file.filename.endswith(".pdf"):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "PDF 파일만 업로드 가능합니다."}
            )

        # 2. 파일 내용 읽기
        content = await file.read()
        
        # 3. 서비스 호출 (실제 분석 로직)
        report_data = ex.pdf_extractor(content, file.filename)
        
        # 4. 결과 반환
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(report_data)
        )

    except Exception as e:
        print(f"Error in controller: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "서버 내부 분석 오류", "error": str(e)}
        )
    finally:
        await file.close()