from pydantic import AnyUrl, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # postgresql://user:password@localhost:5432/mydb
    database_url: AnyUrl

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Настройка Pydantic v2: читаем .env, игнорируем лишние параметры
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Глобальный объект настроек
settings = Settings()
