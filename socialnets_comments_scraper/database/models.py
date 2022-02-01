from datetime import datetime

from pydantic import BaseModel


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
    url: str
    post_id: int
    text: str
    owner_url: str
    created_at_time: datetime
    likes: int


class PostDatabaseModel(BaseModel):
    id: int
    url: str
    owner_id: int
    picture: str
    text: str
    created_at_time: datetime
    likes: int
