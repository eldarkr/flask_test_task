from pydantic import UUID4
from sqlalchemy.orm import Session

from db.models import User
from schemas.enums import UserRole
from schemas.user import UserGet, UserCreate
from services.permissions import Permissions


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user(self, user_id: UUID4) -> UserGet:
        return self.db_session.get(User, user_id)
    
    def get_user_by_email(self, email: str) -> UserGet:
        return self.db_session.query(User).filter(User.email == email).first()
    
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
    
    def delete_user(self, user_id: UUID4, current_user: UserGet):
        if not Permissions.can_manage_all(current_user):
            raise PermissionError("You don't have enough permissions")
        user = self.get_user(user_id)
        self.db_session.delete(user)
        self.db_session.commit()
        return user
