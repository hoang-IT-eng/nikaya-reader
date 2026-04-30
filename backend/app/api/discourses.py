from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.discourse import Discourse
from app.schemas.discourse import DiscourseDetail, DiscourseListItem

router = APIRouter(prefix="/discourses", tags=["discourses"])


@router.get("/", response_model=list[DiscourseListItem])
async def list_discourses(
    volume: int | None = None,
    vagga: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Danh sách bài kinh (không có full_text để tránh payload lớn)."""
    query = select(Discourse)
    if volume:
        query = query.where(Discourse.volume == volume)
    if vagga:
        query = query.where(Discourse.vagga.ilike(f"%{vagga}%"))
    query = query.order_by(Discourse.mn_number)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{mn_number}", response_model=DiscourseDetail)
async def get_discourse(mn_number: int, db: AsyncSession = Depends(get_db)):
    """Chi tiết 1 bài kinh, bao gồm cả bản dịch tiếng Việt nếu có."""
    result = await db.execute(
        select(Discourse).where(Discourse.mn_number == mn_number)
    )
    discourse = result.scalar_one_or_none()
    if not discourse:
        raise HTTPException(status_code=404, detail=f"MN {mn_number} not found")
    return discourse
