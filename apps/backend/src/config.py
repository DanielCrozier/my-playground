"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Runtime settings resolved from environment variables."""

    azure_storage_connection_string: str
    azure_storage_container_name: str = "uploads"
    allow_origins: str = "http://localhost:5173"
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    allowed_content_types: list[str] = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "application/pdf",
        "text/plain",
        "text/csv",
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return a cached Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore[call-arg]
    return _settings
