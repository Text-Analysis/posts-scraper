from datetime import datetime
from typing import List, Optional, TypeVar, Generic
from instaloader import Post

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
    tags: List[str]
    links: List[str]


class PostScrapingModel(BaseModel):
    url: str
    account: AccountScrapingModel
    picture: str
    text: str
    likes: int
    time: datetime
    comments: Optional[List[CommentScrapingModel]]
    tags: List[str]
    links: List[str]


PostInstType = TypeVar('PostInstType', bound=Post)

T: Generic = Generic[PostInstType]
