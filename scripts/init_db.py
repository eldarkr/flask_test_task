import os
import argparse
import subprocess
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.db.models import Base

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DB_TEST_USER = os.getenv("DB_TEST_USER")
DB_TEST_PASSWORD = os.getenv("DB_TEST_PASSWORD")
DB_TEST_HOST = os.getenv("DB_TEST_HOST")
DB_TEST_NAME = os.getenv("DB_TEST_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TEST_DATABASE_URL = f"postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}/{DB_TEST_NAME}"


def run_migrations():
    print("Running Alembic migrations...")
    subprocess.check_call(["alembic", "upgrade", "head"])


def create_tables(engine):
    print("Creating tables using SQLAlchemy...")
    Base.metadata.create_all(engine)


def execute_sql_script(db_url):
    print("Running SQL script to populate mock data...")
    subprocess.check_call(["psql", db_url, "-f", "scripts/populate.sql"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the database.")
    parser.add_argument("--use-test-db", action="store_true", help="Use the test database.")
    args = parser.parse_args()

    if args.use_test_db:
        selected_db_url = TEST_DATABASE_URL
        engine = create_engine(selected_db_url)
        create_tables(engine)
    else:
        selected_db_url = DATABASE_URL
        run_migrations()
        
    print(f"Using database: {selected_db_url}")

    execute_sql_script(selected_db_url)
