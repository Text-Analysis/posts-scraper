from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SocialnetScrapingModel(BaseModel):
    name: str


class EntityScrapingModel(BaseModel):
    name: str
    is_organization: bool


class AccountScrapingModel(BaseModel):
    url: str
    entity: EntityScrapingModel
    socialnet: SocialnetScrapingModel


class CommentScrapingModel(BaseModel):
    url: str
    owner_url: str
    post_url: str
    text: str
    likes: int
    time: datetime


class PostScrapingModel(BaseModel):
    url: str
    account: AccountScrapingModel
    picture: str
    text: str
    likes: int
    time: datetime
    comments: Optional[List[CommentScrapingModel]]
