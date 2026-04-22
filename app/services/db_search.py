from sqlalchemy.orm import Session
from app.db.vector_db import SessionLocal, LaborLaw, Precedent
from app.core.model_loader import ml_engine

class DBSearch:
    def get_related_data(self, query_text: str, top_k: int = 10):
        db = SessionLocal()
        try:
            model = ml_engine.get_bge_model()
            query_embedding = model.encode(query_text).tolist()

            laws = db.query(LaborLaw).order_by(
                LaborLaw.embedding.cosine_distance(query_embedding)
            ).limit(top_k).all()

            precedents = db.query(Precedent).order_by(
                Precedent.embedding.cosine_distance(query_embedding)
            ).limit(top_k).all()

            return laws, precedents
        finally:
            db.close()