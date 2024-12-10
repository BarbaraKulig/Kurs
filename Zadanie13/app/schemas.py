from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    avatar_url: str


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
