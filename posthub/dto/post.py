from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    description: str
    photo: str
    video: str
    publication_date: datetime
