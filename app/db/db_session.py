from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

engine = create_engine(settings.pg_url, echo=settings.DEBUG)
session = sessionmaker(bind=engine)


def get_db():
    with session() as db:
        yield db
