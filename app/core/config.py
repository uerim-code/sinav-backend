from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sinav.db"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    ENVIRONMENT: Literal["development", "production"] = "development"

    # Resend e-posta
    RESEND_API_KEY: str = ""
    MAIL_FROM: str = "bildirim@unvportal.com"

    # Ana backend ile aynı kullanıcı DB'si paylaşılıyorsa
    # MAIN_DATABASE_URL eklenebilir — şimdilik aynı DB'ye bağlanıyor.

    class Config:
        env_file = ".env"


settings = Settings()
