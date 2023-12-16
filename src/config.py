from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int

    MONGO_URL: str
    MONGO_DB: str
    MONGO_URL_TEST: str
    MONGO_DB_TEST: str

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()
