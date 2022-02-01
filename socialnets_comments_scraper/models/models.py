from datetime import datetime
from typing import List
from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    post_id: str
    text: str
    url_user: str
    tags: List[str]
    time: datetime
    links: List[str]

