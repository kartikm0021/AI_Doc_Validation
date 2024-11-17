from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 