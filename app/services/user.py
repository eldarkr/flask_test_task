from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from db.models import User
from schemas.enums import UserRole
from schemas.user import UserGet, UserCreate, UserUpdate, UserLogin
from services.permissions import Permissions


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_all_users(self) -> list[UserGet]:
        return self.db_session.query(User).all()

    def get_user(self, user_id: UUID4) -> UserGet:
        return self.db_session.get(User, user_id)
    
    def get_user_by_email(self, email: EmailStr) -> UserGet:
        return self.db_session.query(User).filter(User.email == email).first()
    
    def get_user_credentials(self, email: EmailStr) -> UserLogin:
        user = self.get_user_by_email(email)
        if not user:
            return None
        return UserLogin(email=user.email, password=user.password)
    
    def create_user(self, user: UserCreate, current_user: UserGet) -> UserGet:
        if not Permissions.can_manage_all(current_user):
            raise PermissionError("You don't have enough permissions")
        user = User(**user.model_dump())
        self.db_session.add(user)
        self.db_session.commit()
        return user
    
    def create_user_with_role_editor(self, user: UserCreate, current_user: UserGet) -> UserGet:
        if not Permissions.can_manage_all(current_user):
            raise PermissionError("You don't have enough permissions")
        user.role = UserRole.EDITOR
        user = User(**user.model_dump())
        self.db_session.add(user)
        self.db_session.commit()
        return user
    
    def update_user(self, user_id: UUID4, user_data: UserUpdate, current_user: UserGet):
        if not Permissions.can_manage_all(current_user):
            raise PermissionError("You don't have permission to update a user")
        query = (
            update(User)
            .where(User.id == user_id)
            .values(**user_data.model_dump(exclude_none=True))
            .returning(User)
        )
        result = self.db_session.execute(query).scalar()
        self.db_session.commit()
        return result
    
    def delete_user(self, user_id: UUID4, current_user: UserGet):
        if not Permissions.can_manage_all(current_user):
            raise PermissionError("You don't have enough permissions")
        user = self.get_user(user_id)
        self.db_session.delete(user)
        self.db_session.commit()
        return user

    def find_user_by_text(self, text: str) -> list[UserGet]:
        query = self.db_session.query(User).filter(
            User.email.ilike(f"%{text}%")
        )
        return query.all()
