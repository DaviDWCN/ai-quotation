import boto3
from typing import Protocol, BinaryIO
from botocore.client import Config
from src.config import settings

class FileStorageAdapter(Protocol):
    async def upload_file(self, file_obj: BinaryIO, filename: str, content_type: str | None = None) -> str:
        """
        Uploads a file and returns the file path/URL.
        """
        ...

class S3StorageAdapter:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.s3_bucket

    async def upload_file(self, file_obj: BinaryIO, filename: str, content_type: str | None = None) -> str:
        import asyncio
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        # boto3 is blocking, so we run it in a separate thread to avoid blocking the event loop.
        await asyncio.to_thread(
            self.s3_client.upload_fileobj,
            file_obj,
            self.bucket,
            filename,
            ExtraArgs=extra_args
        )
        return f"s3://{self.bucket}/{filename}"
