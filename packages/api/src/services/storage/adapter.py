from typing import Protocol, BinaryIO

class FileStorageAdapter(Protocol):
    async def upload_file(self, file_path: str, content: BinaryIO) -> str:
        """Upload a file and return the file URL or identifier."""
        ...

    async def download_file(self, file_id: str) -> bytes:
        """Download a file by its ID/path."""
        ...

    async def get_url(self, file_id: str) -> str:
        """Get the public or presigned URL of a file."""
        ...
