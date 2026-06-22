from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: list[str] = ["https://pixelfuse-frontend.onrender.com"]
    max_upload_files: int = 10
    log_level: str = "info"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PIXELFUSE_",
        env_file_encoding="utf-8",
    )


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
