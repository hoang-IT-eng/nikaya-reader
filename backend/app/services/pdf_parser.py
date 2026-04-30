"""
Parse 3 PDF Middle Discourses thành JSON sạch.

Cấu trúc thật trong PDF:
- Trang đầu bài kinh:
    MN 1
    The Root of All Things
    Mūlapariyāyasutta
    So
    1.1
    I have heard...

- Các trang tiếp theo có running header:
    mūlapariyāyasutta   (hoặc lowercase title)
    <nội dung>
    MN 1
    <số trang>

Chiến lược: parse theo trang, nhận diện trang đầu bài kinh bằng pattern
"MN X\n<Title>\n<Pali>" ở đầu trang.
"""
import re
import json
import fitz  # pymupdf
from pathlib import Path

VOLUMES = [
    {"volume": 1, "file": "Middle-Discourses-sujato-2025-08-25-1.pdf", "mn_range": (1, 50)},
    {"volume": 2, "file": "Middle-Discourses-sujato-2025-08-25-2.pdf", "mn_range": (51, 100)},
    {"volume": 3, "file": "Middle-Discourses-sujato-2025-08-25-3.pdf", "mn_range": (101, 152)},
]

# Pattern nhận diện trang đầu bài kinh: "MN X" ở dòng đầu tiên không trống
MN_START = re.compile(r'^\s*MN\s+(\d+)\s*\n(.+)\n', re.MULTILINE)

# Pattern footer: "MN X\n<số>\n" ở cuối trang
FOOTER_PATTERN = re.compile(r'\nMN\s+\d+\s*\n\d+\s*$')

# Pattern running header ở đầu trang (tên Pali lowercase hoặc title lowercase)
# Thường là 1 dòng ngắn trước nội dung thật
HEADER_PATTERN = re.compile(r'^[a-z][a-zāīūṭṅñṃḷ\s]+\n', re.MULTILINE)

# Vagga headings
VAGGA_PATTERN = re.compile(
    r'(The Chapter on .+|The .+ Chapter|The Greater Chapter .+|The Lesser Chapter .+)',
)


def clean_page_text(text: str) -> str:
    """Bỏ running footer (MN X + số trang ở cuối trang)."""
    # Bỏ footer dạng "\nMN 1\n3\n" ở cuối
    text = re.sub(r'\nMN\s+\d+\s*\n\d+\s*$', '', text.rstrip())
    return text


def is_sutta_start_page(text: str) -> tuple[int, str, str] | None:
    """
    Kiểm tra trang có phải trang đầu bài kinh không.
    Trả về (mn_number, title_en, title_pali) hoặc None.
    
    Trang đầu bài kinh có dạng:
    MN X
    Title English
    Pali title (optional)
    """
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    if not lines:
        return None
    
    # Dòng đầu phải là "MN X"
    m = re.match(r'^MN\s+(\d+)$', lines[0])
    if not m:
        return None
    
    mn_number = int(m.group(1))
    
    if len(lines) < 2:
        return None
    
    title_en = lines[1]
    title_pali = ""
    
    # Dòng thứ 3 có thể là Pali title (chứa ký tự Pali hoặc kết thúc bằng "sutta")
    if len(lines) >= 3:
        candidate = lines[2]
        if re.search(r'sutta|suttanta|ā|ī|ū|ṭ|ṅ|ñ|ṃ|ḷ', candidate, re.IGNORECASE):
            title_pali = candidate
    
    return (mn_number, title_en, title_pali)


def extract_body_from_start_page(text: str, title_en: str, title_pali: str) -> str:
    """Lấy phần nội dung từ trang đầu bài kinh (bỏ MN X, title, pali)."""
    lines = text.strip().split('\n')
    skip = {"MN " + str(i) for i in range(1, 200)}
    
    # Bỏ các dòng header: "MN X", title_en, title_pali
    headers_to_skip = set()
    if title_en:
        headers_to_skip.add(title_en.strip())
    if title_pali:
        headers_to_skip.add(title_pali.strip())
    
    body_lines = []
    skipped_mn = False
    skipped_title = False
    
    for line in lines:
        stripped = line.strip()
        if not skipped_mn and re.match(r'^MN\s+\d+$', stripped):
            skipped_mn = True
            continue
        if not skipped_title and stripped in headers_to_skip:
            skipped_title = True
            continue
        body_lines.append(line)
    
    return '\n'.join(body_lines)


def clean_body_text(text: str) -> str:
    """Làm sạch nội dung bài kinh."""
    # Bỏ running footer cuối trang
    text = re.sub(r'\nMN\s+\d+\s*\n\d+\s*\n?', '\n', text)
    # Bỏ running header đầu trang (tên Pali/title lowercase, 1 dòng ngắn)
    # Pattern: dòng chỉ có chữ thường + ký tự Pali, không có dấu chấm câu
    text = re.sub(r'\n([a-z][a-zāīūṭṅñṃḷ\s]{3,50})\n', '\n', text)
    # Bỏ nhiều dòng trắng
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_into_paragraphs(text: str) -> list[str]:
    """Tách thành đoạn văn."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return [p for p in paragraphs if len(p) > 50]


def parse_volume(volume_info: dict, pdf_dir: str) -> list[dict]:
    """Parse 1 volume PDF."""
    pdf_path = Path(pdf_dir) / volume_info["file"]
    print(f"\nParsing Volume {volume_info['volume']}: {pdf_path.name}")

    doc = fitz.open(str(pdf_path))
    
    # Nhóm các trang theo bài kinh
    discourses_pages: dict[int, dict] = {}  # mn_number -> {info, pages}
    current_mn = None
    current_vagga = ""
    
    for page_num in range(len(doc)):
        page_text = doc[page_num].get_text("text")
        if not page_text.strip():
            continue
        
        # Kiểm tra vagga heading
        vagga_match = VAGGA_PATTERN.search(page_text)
        if vagga_match:
            current_vagga = vagga_match.group(1).strip()
        
        # Kiểm tra trang đầu bài kinh
        result = is_sutta_start_page(page_text)
        if result:
            mn_number, title_en, title_pali = result
            # Chỉ nhận MN trong range của volume này
            mn_min, mn_max = volume_info["mn_range"]
            if mn_min <= mn_number <= mn_max:
                current_mn = mn_number
                body = extract_body_from_start_page(page_text, title_en, title_pali)
                discourses_pages[mn_number] = {
                    "mn_number":  mn_number,
                    "title_en":   title_en,
                    "title_pali": title_pali,
                    "volume":     volume_info["volume"],
                    "vagga":      current_vagga,
                    "raw_pages":  [body],
                }
                continue
        
        # Trang tiếp theo của bài kinh hiện tại
        if current_mn and current_mn in discourses_pages:
            cleaned = clean_page_text(page_text)
            discourses_pages[current_mn]["raw_pages"].append(cleaned)
    
    doc.close()
    
    # Tổng hợp
    discourses = []
    for mn_number in sorted(discourses_pages.keys()):
        info = discourses_pages[mn_number]
        full_text = "\n\n".join(info["raw_pages"])
        full_text = clean_body_text(full_text)
        paragraphs = split_into_paragraphs(full_text)
        
        discourses.append({
            "mn_number":  info["mn_number"],
            "title_en":   info["title_en"],
            "title_pali": info["title_pali"],
            "volume":     info["volume"],
            "vagga":      info["vagga"],
            "full_text":  full_text,
            "paragraphs": paragraphs,
        })
        print(f"  MN {mn_number}: {info['title_en'][:50]} ({len(paragraphs)} đoạn)")
    
    print(f"  Tổng: {len(discourses)} bài kinh")
    return discourses


def parse_all(pdf_dir: str, output_path: str) -> list[dict]:
    """Parse cả 3 PDF, lưu ra JSON."""
    all_discourses = []
    for vol in VOLUMES:
        all_discourses.extend(parse_volume(vol, pdf_dir))

    all_discourses.sort(key=lambda x: x["mn_number"])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_discourses, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(all_discourses)} bài kinh -> {output_path}")
    return all_discourses


if __name__ == "__main__":
    parse_all(
        pdf_dir="data/pdfs",
        output_path="data/processed/discourses.json"
    )
