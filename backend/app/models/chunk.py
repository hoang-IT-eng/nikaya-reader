from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id           = Column(Integer, primary_key=True)
    discourse_id = Column(Integer, ForeignKey("discourses.id"), nullable=False)
    chunk_index  = Column(Integer, nullable=False)
    text         = Column(Text, nullable=False)
    embedding    = Column(Vector(1536), nullable=True)  # OpenAI ada-002

    discourse = relationship("Discourse", back_populates="chunks")
