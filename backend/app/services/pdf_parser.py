"""
Parse 3 PDF Middle Discourses thành JSON sạch.
Cấu trúc: Volume -> Vagga -> MN -> đoạn văn
"""
import re
import json
import fitz  # pymupdf
from pathlib import Path

# Pattern nhận diện bài kinh: "MN 1" hoặc "MN1" ở đầu dòng
MN_PATTERN = re.compile(
    r'^MN\s*(\d+)\s+(.+?)\s*\(([^)]+)\)',
    re.MULTILINE
)
# Pattern nhận diện Vagga (chapter heading)
VAGGA_PATTERN = re.compile(
    r'^The Chapter .+|^TheChapter.+',
    re.MULTILINE
)

VOLUMES = [
    {"volume": 1, "file": "Middle-Discourses-sujato-2025-08-25-1.pdf", "mn_range": (1, 50)},
    {"volume": 2, "file": "Middle-Discourses-sujato-2025-08-25-2.pdf", "mn_range": (51, 100)},
    {"volume": 3, "file": "Middle-Discourses-sujato-2025-08-25-3.pdf", "mn_range": (101, 152)},
]

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Trích text từng trang, kèm số trang."""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        # Bỏ trang trắng
        if text.strip():
            pages.append({"page": i + 1, "text": text})
    doc.close()
    return pages

def clean_text(text: str) -> str:
    """Làm sạch text: fix khoảng trắng, bỏ header/footer lặp."""
    # Fix chữ dính nhau từ PDF (BhikkhuSujato -> Bhikkhu Sujato)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Bỏ nhiều dòng trắng liên tiếp
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_into_paragraphs(text: str) -> list[str]:
    """Tách text thành đoạn văn theo dòng trắng."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return [p for p in paragraphs if len(p) > 30]  # bỏ đoạn quá ngắn

def parse_volume(volume_info: dict, pdf_dir: str) -> list[dict]:
    """Parse 1 volume PDF thành danh sách discourse."""
    pdf_path = Path(pdf_dir) / volume_info["file"]
    print(f"\nParsing Volume {volume_info['volume']}: {pdf_path.name}")

    pages = extract_text_from_pdf(str(pdf_path))
    full_text = "\n".join(p["text"] for p in pages)
    full_text = clean_text(full_text)

    # Tìm tất cả vị trí MN trong text
    mn_matches = list(MN_PATTERN.finditer(full_text))
    print(f"  Tìm thấy {len(mn_matches)} bài kinh")

    discourses = []
    current_vagga = ""

    for i, match in enumerate(mn_matches):
        mn_number = int(match.group(1))
        title_en  = match.group(2).strip()
        title_pali = match.group(3).strip()

        # Lấy nội dung từ vị trí match đến match tiếp theo
        start = match.end()
        end   = mn_matches[i + 1].start() if i + 1 < len(mn_matches) else len(full_text)
        content = full_text[start:end].strip()

        # Tìm vagga gần nhất trước bài kinh này
        vagga_before = full_text[:match.start()]
        vagga_matches = list(VAGGA_PATTERN.finditer(vagga_before))
        if vagga_matches:
            current_vagga = vagga_matches[-1].group(0).strip()

        paragraphs = split_into_paragraphs(content)

        discourses.append({
            "mn_number":   mn_number,
            "title_en":    title_en,
            "title_pali":  title_pali,
            "volume":      volume_info["volume"],
            "vagga":       current_vagga,
            "full_text":   content,
            "paragraphs":  paragraphs,
        })
        print(f"  MN {mn_number}: {title_en} ({len(paragraphs)} đoạn)")

    return discourses

def parse_all(pdf_dir: str, output_path: str):
    """Parse cả 3 PDF, lưu ra JSON."""
    all_discourses = []
    for vol in VOLUMES:
        all_discourses.extend(parse_volume(vol, pdf_dir))

    # Sắp xếp theo số kinh
    all_discourses.sort(key=lambda x: x["mn_number"])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_discourses, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(all_discourses)} bài kinh -> {output_path}")
    return all_discourses

if __name__ == "__main__":
    parse_all(
        pdf_dir="data/pdfs",
        output_path="data/processed/discourses.json"
    )
