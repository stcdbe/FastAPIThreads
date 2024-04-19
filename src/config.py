from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool
    PORT: int
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int

    __MONGO_URL: str = "mongodb://{MONGO_HOST}:{MONGO_PORT}"

    MONGO_HOST: str
    MONGO_PORT: str
    MONGO_DB: str
    MONGO_USER_COLLECTION: str
    MONGO_THREAD_COLLECTION: str

    MONGO_HOST_TEST: str
    MONGO_PORT_TEST: str
    MONGO_DB_TEST: str
    MONGO_USER_COLLECTION_TEST: str
    MONGO_THREAD_COLLECTION_TEST: str

    @property
    def MONGO_URL(self) -> str:
        return self.__MONGO_URL.format(MONGO_HOST=self.MONGO_HOST, MONGO_PORT=self.MONGO_PORT)

    @property
    def MONGO_URL_TEST(self) -> str:
        return self.__MONGO_URL.format(MONGO_HOST=self.MONGO_HOST_TEST, MONGO_PORT=self.MONGO_PORT_TEST)

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()
