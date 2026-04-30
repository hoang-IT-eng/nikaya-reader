from typing import Optional
from pydantic import BaseModel, ConfigDict


class DiscourseDetail(BaseModel):
    """Schema đầy đủ cho 1 bài kinh, bao gồm cả bản dịch tiếng Việt."""
    id: int
    mn_number: int
    title_en: str
    title_pali: Optional[str] = None
    volume: int
    vagga: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    full_text: Optional[str] = None
    title_vi: Optional[str] = None
    full_text_vi: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DiscourseListItem(BaseModel):
    """Schema rút gọn cho danh sách bài kinh (không có full_text)."""
    id: int
    mn_number: int
    title_en: str
    title_pali: Optional[str] = None
    title_vi: Optional[str] = None
    volume: int
    vagga: Optional[str] = None
    page_start: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
