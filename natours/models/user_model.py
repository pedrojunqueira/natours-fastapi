from datetime import datetime
from typing import Optional

from odmantic import Field, Model
from pydantic import validator


class Users(Model):
    name: str
    email: str
    photo: Optional[str]
    password: str
    confirm_password: Optional[str]
    password_changed_at: Optional[datetime]
    password_reset_token: Optional[str]
    password_reset_expire: Optional[str]
    createdAt: datetime = Field(default=datetime.now())

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


