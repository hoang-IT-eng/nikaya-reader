"""
Scraper tải 152 file HTML bản dịch tiếng Việt (Thích Minh Châu) từ budsas.org.

URL pattern: https://budsas.org/uni/u-kinh-trung-bo/trungbo{mn_number:03d}.htm
Output:      backend/data/html_vi/mn{number}.html

Chạy từ thư mục backend/:
    python scripts/scraper.py
"""
import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://budsas.org/uni/u-kinh-trung-bo/trungbo{:03d}.htm"
DEFAULT_OUTPUT_DIR = "data/html_vi"
MN_RANGE = range(1, 153)  # MN 1–152


@dataclass
class ScrapeResult:
    success_count: int = 0
    failed: list[int] = field(default_factory=list)


async def scrape_one(
    client: httpx.AsyncClient,
    mn_number: int,
    output_dir: Path,
    retries: int = 3,
    retry_delay: float = 2.0,
) -> bool:
    """
    Tải 1 file HTML cho bài kinh mn_number.
    Retry tối đa `retries` lần khi gặp lỗi HTTP hoặc timeout.
    Trả về True nếu thành công, False nếu thất bại sau tất cả lần thử.
    """
    url = BASE_URL.format(mn_number)
    output_path = output_dir / f"mn{mn_number}.html"

    for attempt in range(1, retries + 1):
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            output_path.write_bytes(response.content)
            logger.info(f"MN {mn_number}: OK ({len(response.content)} bytes)")
            return True
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning(f"MN {mn_number}: lần thử {attempt}/{retries} thất bại — {e}")
            if attempt < retries:
                await asyncio.sleep(retry_delay)

    logger.error(f"MN {mn_number}: thất bại sau {retries} lần thử — bỏ qua")
    return False


async def scrape_all(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    delay: float = 1.0,
    retries: int = 3,
) -> ScrapeResult:
    """
    Tải toàn bộ 152 file HTML từ budsas.org.
    Delay `delay` giây giữa mỗi request để tránh quá tải server.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    result = ScrapeResult()

    async with httpx.AsyncClient(
        headers={"User-Agent": "Mozilla/5.0 (compatible; NikayaReader/1.0)"},
        follow_redirects=True,
    ) as client:
        for mn_number in MN_RANGE:
            success = await scrape_one(client, mn_number, out, retries=retries)
            if success:
                result.success_count += 1
            else:
                result.failed.append(mn_number)

            # Rate limiting — tránh quá tải server
            if mn_number < max(MN_RANGE):
                await asyncio.sleep(delay)

    print(f"\n=== Kết quả scraping ===")
    print(f"Thành công: {result.success_count}/152")
    if result.failed:
        print(f"Thất bại ({len(result.failed)}): MN {result.failed}")
    else:
        print("Tất cả file đã tải thành công!")

    return result


if __name__ == "__main__":
    asyncio.run(scrape_all())
