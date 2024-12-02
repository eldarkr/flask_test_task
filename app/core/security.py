from jose import jwt
import datetime

from core.settings import settings
from schemas.token import TokenPayload, Token


class SecurityService:
    @staticmethod
    def get_password_hash(bcrypt, password: str) -> str:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def verify_password(bcrypt, password: str, hashed_password: str) -> bool:
        return bcrypt.check_password_hash(hashed_password, password)

    @staticmethod
    def create_access_token(data: str) -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire, "sub": str(data)}
        return jwt.encode(to_encode, settings.SECRET_KEY)


class SecurityJWT:
    @staticmethod
    def verify(token: Token) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            token_data = TokenPayload(**payload)
            print(payload)
            return token_data
        except jwt.JWTError as e:
            print(e)
            return None
