from pydantic import UUID4

from services.user import UserService
from schemas.user import UserGet
from core.security import SecurityJWT


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    def login(self, user_id: UUID4, password: str) -> UserGet:
        user = self.service.get_user(user_id)
        if user and user.password == password:
            return user
        return None

    def get_current_user_by_token(self, token):
        payload = SecurityJWT().verify(token)
        if not payload:
            return None
        user_email = payload.sub
        if user_email is None:
            return None
        return self.service.get_user_by_email(user_email)
