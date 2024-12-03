from pydantic import EmailStr

from services.user import UserService
from schemas.user import UserGet
from core.security import SecurityJWT, SecurityService


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    def login(self, password: str, email: EmailStr) -> UserGet:
        user_credentials = self.service.get_user_credentials(email)
        if not user_credentials \
                or not SecurityService.verify_password(password, user_credentials.password):
            return None
        return SecurityService.create_access_token(email)

    def get_current_user_by_token(self, token):
        payload = SecurityJWT().verify(token)
        if not payload:
            return None
        user_email = payload.sub
        if user_email is None:
            return None
        return self.service.get_user_by_email(user_email)
