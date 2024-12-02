from pydantic import BaseModel, UUID4, EmailStr
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Union[str, UUID4] = None
    email: EmailStr = None
