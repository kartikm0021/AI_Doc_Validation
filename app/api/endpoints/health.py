from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.session import get_db
from app.core.settings import settings

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]

@router.get("/health")
async def health_check(db: DB):
    try:
        result = db.execute(text("SELECT 1"))
        result.scalar()
        return {
            "status": "healthy",
            "database": "connected"
        }
    except SQLAlchemyError as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@router.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"} 