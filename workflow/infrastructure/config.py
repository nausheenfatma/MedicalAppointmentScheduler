import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    @property
    def DATABASE_URL(self):
        password = quote_plus(self.DB_PASSWORD or "")
        return (
            f"postgresql://{self.DB_USER}:"
            f"{password}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()


def validate_env():
    required = {
        "DB_USER": settings.DB_USER,
        "DB_PASSWORD": settings.DB_PASSWORD,
        "DB_HOST": settings.DB_HOST,
        "DB_PORT": settings.DB_PORT,
        "DB_NAME": settings.DB_NAME,
    }

    missing = [k for k, v in required.items() if not v]

    if missing:
        raise ValueError(f"Missing environment variables: {missing}")


validate_env()