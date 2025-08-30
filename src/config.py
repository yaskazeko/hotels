from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None


    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str | None = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = 30

settings = Settings()
