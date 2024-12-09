from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/license_db"
    # Додаткові налаштування можна додати тут: secret keys, JWT settings, etc.
    
    class Config:
        env_file = ".env"

settings = Settings()