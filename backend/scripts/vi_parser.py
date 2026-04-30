"""
Parser trích xuất nội dung tiếng Việt từ các file HTML đã tải về từ budsas.org.

Input:  backend/data/html_vi/mn{number}.html
Output: backend/data/processed/discourses_vi.json

Chạy từ thư mục backend/:
    python scripts/vi_parser.py
"""
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, Tag

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_HTML_DIR = "data/html_vi"
DEFAULT_OUTPUT_JSON = "data/processed/discourses_vi.json"
MIN_CONTENT_LENGTH = 500

# Tags cần loại bỏ (navigation, script, style, v.v.)
TAGS_TO_REMOVE = ["script", "style", "nav", "header", "footer", "noscript"]

# Selectors thường dùng cho navigation trên budsas.org
NAV_CLASSES = ["nav", "navigation", "menu", "header", "footer"]


class ParseError(Exception):
    pass


@dataclass
class ParsedSutta:
    mn_number: int
    title_vi: str
    full_text_vi: str


@dataclass
class ParseResult:
    success_count: int = 0
    failed: list[tuple[int, str]] = field(default_factory=list)  # (mn_number, reason)


def _decode_html(filepath: Path) -> str:
    """Đọc file HTML, thử UTF-8 trước, fallback latin-1."""
    try:
        return filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return filepath.read_text(encoding="latin-1")


def _extract_title(soup: BeautifulSoup) -> str:
    """Trích xuất tiêu đề tiếng Việt từ HTML."""
    # Thử <title> tag trước
    title_tag = soup.find("title")
    if title_tag and title_tag.get_text(strip=True):
        title = title_tag.get_text(strip=True)
        # Bỏ phần "- budsas.org" hoặc tương tự ở cuối
        title = re.sub(r'\s*[-|]\s*budsas.*$', '', title, flags=re.IGNORECASE).strip()
        if title:
            return title

    # Thử <h1>, <h2>, <h3>
    for tag in ["h1", "h2", "h3"]:
        heading = soup.find(tag)
        if heading:
            text = heading.get_text(strip=True)
            if text:
                return text

    return ""


def _clean_text(text: str) -> str:
    """
    Làm sạch text:
    - Bỏ khoảng trắng thừa đầu/cuối mỗi dòng
    - Chuẩn hóa xuống dòng: không quá 2 dòng trắng liên tiếp
    - Bỏ khoảng trắng thừa đầu/cuối toàn bộ text
    """
    # Chuẩn hóa line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Strip từng dòng
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    # Không quá 2 dòng trắng liên tiếp
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _extract_body_text(soup: BeautifulSoup) -> str:
    """Trích xuất nội dung chính từ body, loại bỏ navigation/header/footer."""
    body = soup.find("body")
    if not body:
        body = soup

    # Xóa các tag không cần thiết
    for tag_name in TAGS_TO_REMOVE:
        for tag in body.find_all(tag_name):
            tag.decompose()

    # Xóa các element có class navigation
    for cls in NAV_CLASSES:
        for tag in body.find_all(class_=re.compile(cls, re.IGNORECASE)):
            tag.decompose()

    # Lấy text, tách đoạn bằng \n\n
    paragraphs = []
    for element in body.children:
        if not isinstance(element, Tag):
            continue
        text = element.get_text(separator='\n', strip=True)
        if text:
            paragraphs.append(text)

    full_text = '\n\n'.join(paragraphs)
    return _clean_text(full_text)


def parse_html_file(filepath: str | Path, mn_number: int) -> ParsedSutta:
    """
    Parse 1 file HTML, trả về ParsedSutta.
    Raise ParseError nếu không hợp lệ.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File không tồn tại: {filepath}")

    html = _decode_html(path)
    soup = BeautifulSoup(html, "html.parser")

    title_vi = _extract_title(soup)
    if not title_vi:
        raise ParseError(f"Không tìm thấy tiêu đề trong {path.name}")

    full_text_vi = _extract_body_text(soup)
    if len(full_text_vi) < MIN_CONTENT_LENGTH:
        raise ParseError(
            f"Nội dung quá ngắn ({len(full_text_vi)} ký tự < {MIN_CONTENT_LENGTH}) trong {path.name}"
        )

    return ParsedSutta(
        mn_number=mn_number,
        title_vi=title_vi,
        full_text_vi=full_text_vi,
    )


def parse_all(
    html_dir: str = DEFAULT_HTML_DIR,
    output_json: str = DEFAULT_OUTPUT_JSON,
) -> ParseResult:
    """
    Parse toàn bộ thư mục html_vi/, xuất ra JSON trung gian.
    """
    html_path = Path(html_dir)
    result = ParseResult()
    suttas = []

    for mn_number in range(1, 153):
        filepath = html_path / f"mn{mn_number}.html"
        if not filepath.exists():
            logger.warning(f"MN {mn_number}: file không tồn tại, bỏ qua")
            result.failed.append((mn_number, "file not found"))
            continue

        try:
            sutta = parse_html_file(filepath, mn_number)
            suttas.append({
                "mn_number":   sutta.mn_number,
                "title_vi":    sutta.title_vi,
                "full_text_vi": sutta.full_text_vi,
            })
            result.success_count += 1
            logger.info(f"MN {mn_number}: OK — {sutta.title_vi[:40]}")
        except (ParseError, FileNotFoundError) as e:
            logger.error(f"MN {mn_number}: {e}")
            result.failed.append((mn_number, str(e)))

    # Lưu JSON
    out_path = Path(output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(suttas, f, ensure_ascii=False, indent=2)

    print(f"\n=== Kết quả parsing ===")
    print(f"Thành công: {result.success_count}")
    if result.failed:
        print(f"Thất bại ({len(result.failed)}): {[mn for mn, _ in result.failed]}")
    print(f"Output: {output_json}")

    return result


if __name__ == "__main__":
    parse_all()
