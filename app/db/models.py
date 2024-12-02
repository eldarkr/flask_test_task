import uuid
from pydantic import UUID4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from schemas.enums import UserRole


class Base(DeclarativeBase):
    __abstract__ = True


class BaseId(Base):
    __abstract__ = True

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class User(BaseId):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles"), nullable=False, default=UserRole.VIEWER
    )
    
    articles: Mapped[list["Article"]] = relationship("Article", back_populates="owner")


class Article(BaseId):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    owner_id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    owner: Mapped[User] = relationship("User", back_populates="articles")
