from pydantic import BaseModel
from datetime import datetime


class PostView(BaseModel):
    title: str
    description: str
    content: str
    publication_date: datetime

    class Config:
        orm_mode = True
