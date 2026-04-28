from sqlalchemy import Column, Integer, Text, DateTime, func
from app.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id         = Column(Integer, primary_key=True)
    mn_number  = Column(Integer, nullable=False)
    note       = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
