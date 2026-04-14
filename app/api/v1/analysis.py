#계약서 분석 엔드포인트
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_extractor import pdf_extractor

router = APIRouter()

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    # 1. 파일 확장자 체크
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다. (JPG, PNG, PDF만 가능)")

    # 2. 파일 읽기
    content = await file.read()
    
    # 3. OCR 실행
    extracted_text = pdf_extractor.extract_text(content, file.filename)
    
    if not extracted_text:
        raise HTTPException(status_code=500, detail="텍스트 추출에 실패했습니다.")

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "message": "텍스트 추출 완료. 이제 독소 조항 분석을 시작할 수 있습니다."
    }