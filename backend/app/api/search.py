from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from app.database import get_db
from app.models.discourse import Discourse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
async def search(q: str, db: AsyncSession = Depends(get_db)):
    """Full-text search dùng pg_trgm"""
    result = await db.execute(
        select(
            Discourse.mn_number, Discourse.title_en,
            Discourse.title_pali, Discourse.volume, Discourse.vagga,
            func.similarity(Discourse.full_text, q).label("score")
        )
        .where(func.similarity(Discourse.full_text, q) > 0.05)
        .order_by(text("score DESC"))
        .limit(20)
    )
    return result.mappings().all()
