from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    email_verification_secret: str
    rate_limit: int = 10  # Domyślna wartość dla limitu żądań

    class Config:
        env_file = ".env"


settings = Settings()

# Dodajemy BaseSettings do __all__
__all__ = ["Settings", "settings", "BaseSettings"]
