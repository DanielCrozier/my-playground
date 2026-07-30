"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.config import Settings, get_settings
from src.main import create_app


def make_test_settings(**overrides: object) -> Settings:
    """Create a Settings instance with test defaults."""
    defaults: dict[str, object] = {
        "azure_storage_connection_string": (
            "DefaultEndpointsProtocol=https;"
            "AccountName=devstoreaccount1;"
            "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
            "BlobEndpoint=https://devstoreaccount1.blob.core.windows.net;"
        ),
        "azure_storage_container_name": "test-uploads",
        "allow_origins": "http://localhost:5173",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


@pytest.fixture()
def test_settings() -> Settings:
    """Return test settings."""
    return make_test_settings()


@pytest.fixture()
def client(test_settings: Settings) -> TestClient:
    """Return a TestClient with overridden settings."""
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: test_settings
    return TestClient(app, raise_server_exceptions=False)
