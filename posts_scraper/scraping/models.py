from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CommentScrapingModel(BaseModel):
    url: str
    owner_url: str
    post_url: str
    text: str
    likes: int
    created_at_time: datetime


class PostScrapingModel(BaseModel):
    url: str
    owner_url: str
    picture: str
    text: str
    likes: int
    created_at_time: datetime
    comments: Optional[List[CommentScrapingModel]]
