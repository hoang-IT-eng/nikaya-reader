"""
Pipeline tổng hợp: scrape → parse → import tiếng Việt.

Chạy từ thư mục backend/:
    python scripts/import_vietnamese_pipeline.py

Các bước:
1. Tải 152 file HTML từ budsas.org → data/html_vi/
2. Parse HTML → data/processed/discourses_vi.json
3. Import JSON vào PostgreSQL (UPDATE discourses)
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.scraper import scrape_all
from scripts.vi_parser import parse_all
from scripts.vi_importer import import_vietnamese


async def main():
    print("=" * 50)
    print("=== Bước 1: Tải HTML từ budsas.org ===")
    print("=" * 50)
    scrape_result = await scrape_all(
        output_dir="data/html_vi",
        delay=1.0,
    )
    if scrape_result.failed:
        print(f"\nCảnh báo: {len(scrape_result.failed)} file tải thất bại: {scrape_result.failed}")
        print("Tiếp tục với các file đã tải được...\n")

    print("\n" + "=" * 50)
    print("=== Bước 2: Parse HTML → JSON ===")
    print("=" * 50)
    parse_result = parse_all(
        html_dir="data/html_vi",
        output_json="data/processed/discourses_vi.json",
    )
    if parse_result.failed:
        print(f"\nCảnh báo: {len(parse_result.failed)} file parse thất bại")

    print("\n" + "=" * 50)
    print("=== Bước 3: Import vào PostgreSQL ===")
    print("=" * 50)
    import_result = await import_vietnamese(
        json_path="data/processed/discourses_vi.json",
    )

    print("\n" + "=" * 50)
    print("=== Hoàn tất! ===")
    print(f"Scrape: {scrape_result.success_count}/152 thành công")
    print(f"Parse:  {parse_result.success_count} thành công")
    print(f"Import: {import_result.updated_count} bài kinh đã cập nhật tiếng Việt")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
