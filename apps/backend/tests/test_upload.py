"""Tests for the upload endpoint."""

import io
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


def _make_file(
    content: bytes = b"hello",
    filename: str = "test.txt",
    content_type: str = "text/plain",
) -> tuple[str, tuple[str, io.BytesIO, str]]:
    return ("file", (filename, io.BytesIO(content), content_type))


class TestUploadEndpoint:
    """Tests for POST /upload."""

    def test_upload_success(self, client: TestClient) -> None:
        """Valid file upload should return 201 with a blob_name."""
        mock_blob_client = MagicMock()
        mock_container = MagicMock()
        mock_container.get_blob_client.return_value = mock_blob_client
        mock_service = MagicMock()
        mock_service.get_container_client.return_value = mock_container

        with patch("src.routers.upload.get_blob_service_client", return_value=mock_service):
            response = client.post("/upload", files=[_make_file()])

        assert response.status_code == 201
        data = response.json()
        assert "blob_name" in data
        assert data["blob_name"].endswith("-test.txt")
        mock_blob_client.upload_blob.assert_called_once()

    def test_upload_disallowed_content_type(self, client: TestClient) -> None:
        """Files with disallowed content types should return 415."""
        response = client.post(
            "/upload",
            files=[_make_file(content_type="application/x-executable")],
        )
        assert response.status_code == 415

    def test_upload_file_too_large(self, client: TestClient) -> None:
        """Files exceeding the size limit should return 413."""
        from src.config import Settings, get_settings
        from src.main import create_app

        small_limit_settings = Settings(  # type: ignore[call-arg]
            azure_storage_connection_string=(
                "DefaultEndpointsProtocol=https;"
                "AccountName=devstoreaccount1;"
                "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
                "BlobEndpoint=https://devstoreaccount1.blob.core.windows.net;"
            ),
            azure_storage_container_name="test-uploads",
            allow_origins="http://localhost:5173",
            max_upload_size_bytes=5,  # only 5 bytes allowed
        )
        app = create_app()
        app.dependency_overrides[get_settings] = lambda: small_limit_settings
        small_client = TestClient(app, raise_server_exceptions=False)

        mock_blob_client = MagicMock()
        mock_container = MagicMock()
        mock_container.get_blob_client.return_value = mock_blob_client
        mock_service = MagicMock()
        mock_service.get_container_client.return_value = mock_container

        with patch("src.routers.upload.get_blob_service_client", return_value=mock_service):
            response = small_client.post(
                "/upload",
                files=[_make_file(content=b"more than 5 bytes")],
            )

        assert response.status_code == 413

    def test_upload_azure_error_returns_502(self, client: TestClient) -> None:
        """Azure errors should surface as 502 Bad Gateway."""
        from azure.core.exceptions import AzureError

        mock_blob_client = MagicMock()
        mock_blob_client.upload_blob.side_effect = AzureError("boom")
        mock_container = MagicMock()
        mock_container.get_blob_client.return_value = mock_blob_client
        mock_service = MagicMock()
        mock_service.get_container_client.return_value = mock_container

        with patch("src.routers.upload.get_blob_service_client", return_value=mock_service):
            response = client.post("/upload", files=[_make_file()])

        assert response.status_code == 502

    def test_upload_no_file_returns_422(self, client: TestClient) -> None:
        """Missing file field should return 422 Unprocessable Entity."""
        response = client.post("/upload")
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "content_type",
        [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/webp",
            "application/pdf",
            "text/plain",
            "text/csv",
        ],
    )
    def test_upload_allowed_content_types(
        self, client: TestClient, content_type: str
    ) -> None:
        """All allowed content types should succeed."""
        mock_blob_client = MagicMock()
        mock_container = MagicMock()
        mock_container.get_blob_client.return_value = mock_blob_client
        mock_service = MagicMock()
        mock_service.get_container_client.return_value = mock_container

        with patch("src.routers.upload.get_blob_service_client", return_value=mock_service):
            response = client.post(
                "/upload",
                files=[_make_file(content_type=content_type)],
            )

        assert response.status_code == 201
