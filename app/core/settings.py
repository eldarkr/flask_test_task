from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    UVICORN_HOST: str
    UVICORN_PORT: int

    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    DB_TEST_HOST: str
    DB_TEST_NAME: str
    DB_TEST_USER: str
    DB_TEST_PASSWORD: str
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    DEBUG: bool

    @property
    def pg_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}/{self.DB_NAME}"
        )
        
    @property
    def test_pg_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_TEST_USER}:{self.DB_TEST_PASSWORD}@"
            f"localhost/{self.DB_TEST_NAME}"
        )


settings = Settings()
