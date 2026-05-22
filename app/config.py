from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    MODEL_NAME: str
    EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"

    GOOGLE_CREDENTIALS_PATH: str = "C:\\Github Repo\\hr_system\\app\\credentials.json"
    GOOGLE_TOKEN_PATH: str = "C:\\Github Repo\\hr_system\\app\\token.json"

    SQLITE_DB: str

    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"


settings = Settings()