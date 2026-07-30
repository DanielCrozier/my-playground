"""File upload router."""

import uuid
from typing import Annotated

from azure.core.exceptions import AzureError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from src.config import Settings, get_settings
from src.storage import get_blob_service_client

router = APIRouter(prefix="/upload", tags=["upload"])

_CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file to Azure Blob Storage",
)
async def upload_file(
    file: UploadFile,
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    """Accept a multipart upload and stream it to Azure Blob Storage.

    Returns the blob name on success.
    """
    if file.content_type not in settings.allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Content type '{file.content_type}' is not allowed. "
                f"Allowed types: {settings.allowed_content_types}"
            ),
        )

    blob_name = f"{uuid.uuid4()}-{file.filename or 'upload'}"
    client = get_blob_service_client(settings.azure_storage_connection_string)
    container = client.get_container_client(settings.azure_storage_container_name)

    try:
        blob_client = container.get_blob_client(blob_name)
        total_bytes = 0

        async def _read_chunks() -> bytes:
            nonlocal total_bytes
            chunks: list[bytes] = []
            while True:
                chunk = await file.read(_CHUNK_SIZE)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > settings.max_upload_size_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail=(
                            f"File exceeds maximum allowed size of "
                            f"{settings.max_upload_size_bytes} bytes."
                        ),
                    )
                chunks.append(chunk)
            return b"".join(chunks)

        data = await _read_chunks()
        blob_client.upload_blob(
            data,
            overwrite=False,
            content_settings=None,
        )
    except HTTPException:
        raise
    except AzureError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to upload to Azure Blob Storage: {exc}",
        ) from exc

    return {"blob_name": blob_name}
