from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models.bookmark import Bookmark

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

class BookmarkIn(BaseModel):
    mn_number: int
    note: str = ""

@router.get("/")
async def list_bookmarks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bookmark).order_by(Bookmark.created_at.desc()))
    return result.scalars().all()

@router.post("/")
async def add_bookmark(data: BookmarkIn, db: AsyncSession = Depends(get_db)):
    bookmark = Bookmark(mn_number=data.mn_number, note=data.note)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark

@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bookmark).where(Bookmark.id == bookmark_id))
    bookmark = result.scalar_one_or_none()
    if bookmark:
        await db.delete(bookmark)
        await db.commit()
    return {"ok": True}
