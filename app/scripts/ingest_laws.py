# 벡터 DB 데이터 적재용 스크립트
import pandas as pd
import re
import os
import logging
from sqlalchemy.orm import Session
from app.db.vector_db import SessionLocal
from app.db.vector_db import LaborLaw
from app.core.model_loader import ml_engine

logger = logging.getLogger("uvicorn.error")

def parse_law_details(text: str):
    """
    정규표현식을 이용한 조, 항, 호 상세 파싱 로직
    """
    # 조: 제12조, 제12조의2 등 처리
    article = re.search(r'제\d+조(?:의\d+)?', text)
    article_num = article.group() if article else ""
    
    # 항: ①, ②, ③ 등 원문자
    paragraph = re.search(r'[\u2460-\u246b]', text)
    paragraph_num = paragraph.group() if paragraph else ""
    
    # 호: 1., 2. 형태 (공백 뒤에 오는 숫자+점)
    item = re.search(r'(?<=\s)\d+\.', text)
    item_num = item.group() if item else ""
    
    return article_num, paragraph_num, item_num

def ingest_labor_laws(file_path: str):
    """
    벡터 DB 데이터 적재 메인 함수
    """
    db: Session = SessionLocal()
    # BGE-M3 모델 가져오기
    embed_model = ml_engine.get_bge_model()
    
    try:
        # 파일 존재 여부를 먼저 확인하고, 없으면 절대 경로로 재시도
        if not os.path.exists(file_path):
            # 현재 파일(ingest_laws.py)의 위치를 기준으로 프로젝트 루트를 찾아 경로 재설정
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_path, "data", "근로기준법_조항.csv")
            
        logger.info(f"🔎 파일 읽기 시도 중: {os.path.abspath(file_path)}")
        
        df = pd.read_csv(file_path)
        
        laws_to_add = []
        
        logger.info(f"⏳ {len(df)}건의 법령 데이터 벡터화 시작...")

        for _, row in df.iterrows():
            raw_text = row['text']
            article, paragraph, item = parse_law_details(raw_text)
            
            # 2. 검색 최적화를 위한 참조명 생성
            # 예: 근로기준법 제2조 ① 1.
            full_ref = f"근로기준법 {article} {paragraph} {item}".strip()
            
            # 3. 벡터화 (BGE-M3)
            # 텍스트와 레퍼런스를 함께 넣어 문맥을 강화합니다.
            combined_text = f"{full_ref} | {raw_text}"
            embedding = embed_model.encode(combined_text).tolist()

            # 4. ORM 객체 매핑
            law_entry = LaborLaw(
                article_num=article,
                paragraph_num=paragraph,
                item_num=item,
                law_content=raw_text,
                full_reference=full_ref,
                embedding=embedding
            )
            laws_to_add.append(law_entry)

        # 5. 벌크 저장 (성능 최적화)
        db.bulk_save_objects(laws_to_add)
        db.commit()
        logger.info(f"✅ 법령 데이터 {len(laws_to_add)}건 적재 완료!")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ 데이터 적재 중 치명적 오류: {e}")
        raise e
    finally:
        db.close()