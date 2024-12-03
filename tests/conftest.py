import uuid
import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.routes.article_routes import article_bp
from app.db.models import Article, User
from app.services.user import UserService
from app.services.auth import AuthService
from app.core.settings import settings
from app.core.security import SecurityService
from app.schemas.user import UserGet
from app.schemas.enums import UserRole
from app.schemas.article import ArticleGet

engine = create_engine(settings.test_pg_url, echo=settings.DEBUG)
session_factory = sessionmaker(autoflush=False, bind=engine)
Session = scoped_session(session_factory)


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(article_bp)
    return app.test_client()


@pytest.fixture
def articles():
    session = Session()
    try:
        return session.query(Article).all()
    finally:
        session.close()


@pytest.fixture
def users():
    session = Session()
    try:
        return session.query(User).all()
    finally:
        session.close()


# @pytest.fixture
# def auth_service():
#     session = SessionLocal
#     user_service = UserService(session)
#     return AuthService(user_service)


@pytest.fixture
def auth_service():
    session = Session()
    try:
        user_service = UserService(session)
        return AuthService(user_service)
    finally:
        Session.remove()


@pytest.fixture
def security_service():
    return SecurityService()


@pytest.fixture
def email():
    return "test@example.com"


@pytest.fixture
def password():
    return "password123"


@pytest.fixture
def admin_user():
    return UserGet(id=uuid.uuid4(), email="a@gmail.com", role=UserRole.ADMIN.value)


@pytest.fixture
def editor_user():
    return UserGet(id=uuid.uuid4(), email="a1@gmail.com", role=UserRole.EDITOR.value)


USER_ID = uuid.uuid4()


@pytest.fixture
def regular_user():
    return UserGet(id=USER_ID, email="a2@gmail.com", role=UserRole.VIEWER.value)


@pytest.fixture
def article():
    return ArticleGet(id=uuid.uuid4(), owner_id=USER_ID, title="Test", content="Test")
