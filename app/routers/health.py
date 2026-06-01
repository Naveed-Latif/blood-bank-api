from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(
    tags=["health"]
)


@router.get("/health")
async def health():
    """Check the health of the server and database connection."""
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()

        return {
            "status": "ok",
            "db": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
