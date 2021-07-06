from enum import Enum
from typing import Optional, List
from pydantic import EmailStr, UUID4
from app.models.core import IDModelMixin, CoreModel



class UserBase(CoreModel):
    """
    All common characteristics of our Users resource
    """
    email: Optional[EmailStr]

class UserCreate(UserBase):
    email: EmailStr
    password: str
    is_active: Optional[bool] = False
    confirmation: Optional[UUID4]
    

class UserUpdate(UserBase):
    email: Optional[EmailStr]


class UserInDB(IDModelMixin, UserBase):
    email: EmailStr
    is_active: bool
    confirmation: Optional[UUID4]
    hashed_password: str


class UserPublic(IDModelMixin, UserBase):
    pass
