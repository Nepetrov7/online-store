from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.config import settings

engine = create_engine(str(settings.database_url), echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """
    Зависимость для FastAPI.
    Возвращает объект сессии, который закрывается после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
