"""
Importer nhập dữ liệu tiếng Việt từ JSON vào PostgreSQL.

Đọc file discourses_vi.json và UPDATE bảng discourses theo mn_number.
Toàn bộ quá trình là atomic — nếu có lỗi, rollback toàn bộ.

Chạy từ thư mục backend/ (sau khi đã chạy vi_parser.py):
    python scripts/vi_importer.py
"""
import asyncio
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.config import settings
from app.models.discourse import Discourse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_JSON_PATH = "data/processed/discourses_vi.json"


@dataclass
class ImportResult:
    updated_count: int = 0
    skipped: list[int] = field(default_factory=list)  # mn_number không tìm thấy trong DB


async def import_vietnamese(
    json_path: str = DEFAULT_JSON_PATH,
) -> ImportResult:
    """
    Đọc JSON và UPDATE bảng discourses theo mn_number.
    Dùng 1 transaction duy nhất — atomic.
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"File JSON không tồn tại: {json_path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    engine = create_async_engine(settings.database_url, echo=False)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    result = ImportResult()

    async with session_maker() as session:
        async with session.begin():
            for item in data:
                mn_number = item["mn_number"]
                title_vi = item.get("title_vi", "")
                full_text_vi = item.get("full_text_vi", "")

                # Kiểm tra bản ghi tồn tại
                from sqlalchemy import select
                existing = await session.execute(
                    select(Discourse.id).where(Discourse.mn_number == mn_number)
                )
                if existing.scalar_one_or_none() is None:
                    logger.warning(f"MN {mn_number}: không tìm thấy trong DB, bỏ qua")
                    result.skipped.append(mn_number)
                    continue

                # UPDATE
                await session.execute(
                    update(Discourse)
                    .where(Discourse.mn_number == mn_number)
                    .values(title_vi=title_vi, full_text_vi=full_text_vi)
                )
                result.updated_count += 1
                logger.info(f"MN {mn_number}: cập nhật OK")

    await engine.dispose()

    print(f"\n=== Kết quả import tiếng Việt ===")
    print(f"Cập nhật thành công: {result.updated_count}")
    if result.skipped:
        print(f"Bỏ qua ({len(result.skipped)}): MN {result.skipped}")
    else:
        print("Tất cả bài kinh đã được cập nhật!")

    return result


async def main():
    await import_vietnamese()


if __name__ == "__main__":
    asyncio.run(main())
