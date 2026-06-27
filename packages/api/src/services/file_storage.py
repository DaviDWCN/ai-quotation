from typing import Protocol, BinaryIO
import boto3
from botocore.exceptions import ClientError
import asyncio

class FileStorageAdapter(Protocol):
    async def upload_file(self, file_obj: BinaryIO, bucket: str, object_name: str) -> str:
        """Upload a file to storage and return the URL or identifier."""
        ...

    async def download_file(self, bucket: str, object_name: str) -> bytes:
        """Download a file from storage."""
        ...

class S3StorageAdapter:
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region_name: str = "us-east-1"):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

    async def upload_file(self, file_obj: BinaryIO, bucket: str, object_name: str) -> str:
        try:
            await asyncio.to_thread(self.s3_client.upload_fileobj, file_obj, bucket, object_name)
            return f"{bucket}/{object_name}"
        except ClientError as e:
            # Handle error appropriately
            raise e

    async def download_file(self, bucket: str, object_name: str) -> bytes:
        try:
            response = await asyncio.to_thread(self.s3_client.get_object, Bucket=bucket, Key=object_name)
            return cast(bytes, response['Body'].read())
        except ClientError as e:
            raise e

# Add cast import for mypy in download_file if needed
from typing import cast
