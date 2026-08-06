"""Azure Blob Storage client helpers."""

from azure.storage.blob import BlobServiceClient


def get_blob_service_client(connection_string: str) -> BlobServiceClient:
    """Create a BlobServiceClient from a connection string."""
    return BlobServiceClient.from_connection_string(connection_string)
