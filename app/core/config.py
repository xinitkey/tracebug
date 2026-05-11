from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tracebug API"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./tracebug.db"
    secret_key: str = "8e72ce26e2685a0e067dda353d642ca466cbc59410922f209793b4c8cfe0507c"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
