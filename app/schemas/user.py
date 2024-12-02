from pydantic import UUID4, BaseModel, EmailStr
from typing import Optional

from schemas.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    
    
class UserCreate(UserBase):
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.VIEWER

class UserGet(UserBase):
    id: UUID4
    role: UserRole


class UserLogin(UserBase):
    password: str

