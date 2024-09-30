import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Настройки путей
    url_auth: str = "/authorization"
    url_path_main: str = "/photo-base/v0.1"
    url_path_admin: str = "/photo-base/v0.1/admin"

    # Настройки базы данных
    db_url: str = f"sqlite+aiosqlite:///{os.getenv("DB_NAME")}.db"
    db_echo: bool = False

    # Настройки секретных ключей для генерации токена
    password_secret: str = os.getenv("PASSWORD_TOKEN_SECRET")
    verification_secret: str = os.getenv("VERIFICATION_TOKEN_SECRET")

    # Настройка времени для токена (действие access-token)
    lifetime_seconds: int = 3600

    # Настройка логов
    filename_log: str = "LOG_API_V0.1.log"
    filemod: str = "w"
    format_log: str = "%(asctime)s %(levelname)s %(message)s"

    # Настройка пути для авторизации
    @property
    def bearer_token_url(self) -> str:
        parts = (self.url_path_main, self.url_auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


settings = Settings()
