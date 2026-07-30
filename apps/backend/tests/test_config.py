"""Tests for application configuration."""

import os

import pytest

from src.config import Settings, get_settings


class TestSettings:
    """Tests for Settings loading."""

    def test_defaults(self) -> None:
        """Default values should be applied."""
        s = Settings(azure_storage_connection_string="conn")  # type: ignore[call-arg]
        assert s.azure_storage_container_name == "uploads"
        assert s.max_upload_size_bytes == 10 * 1024 * 1024

    def test_override_via_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Environment variables should override defaults."""
        monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "env-conn")
        monkeypatch.setenv("AZURE_STORAGE_CONTAINER_NAME", "my-container")

        s = Settings()  # type: ignore[call-arg]
        assert s.azure_storage_connection_string == "env-conn"
        assert s.azure_storage_container_name == "my-container"

    def test_get_settings_caches(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_settings should return the same instance on repeated calls."""
        import src.config as cfg_module

        monkeypatch.setattr(cfg_module, "_settings", None)
        monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "cache-conn")

        first = get_settings()
        second = get_settings()
        assert first is second
