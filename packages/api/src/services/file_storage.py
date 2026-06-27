from typing import Protocol, BinaryIO
import boto3
from botocore.client import Config

class FileStorageAdapter(Protocol):
    def upload_file(self, bucket_name: str, object_name: str, data: BinaryIO, content_type: str) -> str:
        """Upload a file to storage and return the URL or path."""
        ...

class MinIOAdapter:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        self.client = boto3.client(
            's3',
            endpoint_url=f"{'https' if secure else 'http'}://{endpoint}",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1' # Default for MinIO
        )

    def upload_file(self, bucket_name: str, object_name: str, data: BinaryIO, content_type: str) -> str:
        self.client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=data,
            ContentType=content_type
        )
        return f"{bucket_name}/{object_name}"

    def ensure_bucket_exists(self, bucket_name: str) -> None:
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except:
            self.client.create_bucket(Bucket=bucket_name)
