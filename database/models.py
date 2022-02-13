from datetime import datetime

from pydantic import BaseModel
from typing import List


class SocialnetDatabaseModel(BaseModel):
    id: int
    name: str


class EntityDatabaseModel(BaseModel):
    id: int
    name: str
    is_organization: bool


class AccountDatabaseModel(BaseModel):
    id: int
    url: str
    entity_id: int
    socialnet_id: int


class CommentDatabaseModel(BaseModel):
    id: int
    post_id: int
    text: str
    url: str
    owner_url: str
    time: datetime
    likes: int
    tags: List[str]
    links: List[str]


class PostDatabaseModel(BaseModel):
    id: int
    url: str
    owner_id: int
    picture: str
    text: str
    time: datetime
    likes: int
    tags: List[str]
    links: List[str]
