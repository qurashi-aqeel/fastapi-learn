from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Literal


# Pydantic Post Base model
class PostBase(BaseModel):
    title: str
    content: str
    draft: bool = False


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRes(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(extra='forbid')

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None


class PostRes(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserRes

    model_config = ConfigDict(extra='forbid')


class Vote(BaseModel):
    post_id: int
    direction: Literal[-1, 0, 1]
    # -1 = downvote, 0 = remove, 1 = upvote
