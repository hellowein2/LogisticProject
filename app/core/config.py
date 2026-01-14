from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    REDIS_URL: str
    RABBITMQ_URL: str
    PROJECT_NAME: str = "delivery-service"
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CBR_URL: str

    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
