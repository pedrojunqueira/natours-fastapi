from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

class EmailSchema(BaseModel):
    email: EmailStr


class PasswordSchema(BaseModel):
    password: str
    confirm_password: str


class UpdatePasswordSchema(BaseModel):
    current_password: str
    password: str
    confirm_password: str
