from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE: int

    EMAILHUNTER_API_KEY: str

    class Config:
        env_file = "test.env"


def get_settings() -> Settings:
    return Settings()
