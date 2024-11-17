from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from typing import Annotated

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="FastAPI PostgreSQL App",
    description="A simple FastAPI application with PostgreSQL integration",
    version="1.0.0"
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use Annotated for better type hints (new in FastAPI 0.115.x)
DB = Annotated[SessionLocal, Depends(get_db)]

@app.get("/health")
async def health_check(db: DB):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
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

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI PostgreSQL Application"} 