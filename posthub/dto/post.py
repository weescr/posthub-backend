from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    description: str
    content: str
    publication_date: datetime
