"""
Import dữ liệu từ JSON đã parse vào PostgreSQL.
Chạy sau khi pdf_parser.py đã tạo ra discourses.json
"""
import asyncio
import json
from app.database import engine, async_session_maker
from app.models import Discourse, Chunk
from app.database import Base

async def create_tables():
    """Tạo bảng và enable extensions."""
    async with engine.begin() as conn:
        await conn.execute(__import__('sqlalchemy').text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.execute(__import__('sqlalchemy').text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

async def import_discourses(json_path: str):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    async with async_session_maker() as session:
        for item in data:
            discourse = Discourse(
                mn_number  = item["mn_number"],
                title_en   = item["title_en"],
                title_pali = item.get("title_pali", ""),
                volume     = item["volume"],
                vagga      = item.get("vagga", ""),
                full_text  = item["full_text"],
            )
            session.add(discourse)
        await session.commit()
    print(f"Imported {len(data)} discourses.")

async def main():
    await create_tables()
    await import_discourses("data/processed/discourses.json")

if __name__ == "__main__":
    asyncio.run(main())
