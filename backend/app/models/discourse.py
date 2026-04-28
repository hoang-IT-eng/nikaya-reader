from sqlalchemy import Column, Integer, Text, Index
from sqlalchemy.orm import relationship
from app.database import Base

class Discourse(Base):
    __tablename__ = "discourses"

    id         = Column(Integer, primary_key=True)
    mn_number  = Column(Integer, unique=True, nullable=False)
    title_en   = Column(Text, nullable=False)
    title_pali = Column(Text)
    volume     = Column(Integer, nullable=False)  # 1, 2, 3
    vagga      = Column(Text)
    page_start = Column(Integer)
    page_end   = Column(Integer)
    full_text  = Column(Text)

    chunks = relationship("Chunk", back_populates="discourse", cascade="all, delete-orphan")

# GIN index cho pg_trgm full-text search
Index("ix_discourses_trgm", Discourse.full_text, postgresql_using="gin",
      postgresql_ops={"full_text": "gin_trgm_ops"})
