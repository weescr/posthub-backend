from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from posthub.db.base import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    photo = Column(String, nullable=True)
    video = Column(String, nullable=True)  
    publication_date = Column(DateTime(timezone=True), server_default=func.now())
