from datetime import datetime
from typing import List
from pydantic import BaseModel


class Comment(BaseModel):
    Id: int
    PostId: str
    Text: str
    UrlUser: str
    Tags: List[str]
    Time: datetime
    Links: List[str]
