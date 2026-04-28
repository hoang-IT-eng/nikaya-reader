from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.discourse import Discourse

router = APIRouter(prefix="/discourses", tags=["discourses"])

@router.get("/")
async def list_discourses(
    volume: int | None = None,
    vagga: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(
        Discourse.id, Discourse.mn_number, Discourse.title_en,
        Discourse.title_pali, Discourse.volume, Discourse.vagga,
        Discourse.page_start
    )
    if volume:
        query = query.where(Discourse.volume == volume)
    if vagga:
        query = query.where(Discourse.vagga.ilike(f"%{vagga}%"))
    query = query.order_by(Discourse.mn_number)
    result = await db.execute(query)
    return result.mappings().all()

@router.get("/{mn_number}")
async def get_discourse(mn_number: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Discourse).where(Discourse.mn_number == mn_number)
    )
    discourse = result.scalar_one_or_none()
    if not discourse:
        raise HTTPException(status_code=404, detail=f"MN {mn_number} not found")
    return discourse
