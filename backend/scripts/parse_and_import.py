"""
One-shot script: parse PDFs then import into DB.
Run from backend/ directory:
    python scripts/parse_and_import.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent to path so app imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.pdf_parser import parse_all
from app.services.importer import create_tables, import_discourses

PDF_DIR = "data/pdfs"
JSON_OUT = "data/processed/discourses.json"


async def main():
    print("=== Step 1: Parse PDFs ===")
    parse_all(pdf_dir=PDF_DIR, output_path=JSON_OUT)

    print("\n=== Step 2: Create DB tables ===")
    await create_tables()

    print("\n=== Step 3: Import discourses ===")
    await import_discourses(JSON_OUT)

    print("\nAll done!")


if __name__ == "__main__":
    asyncio.run(main())
