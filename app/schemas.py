from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


# Pydantic Post Base model
class PostBase(BaseModel):
    title: str
    content: str
    draft: bool = False


class PostCreate(PostBase):
    pass


class PostRes(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(extra='forbid')


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
