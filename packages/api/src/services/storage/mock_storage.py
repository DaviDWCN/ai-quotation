import os
import shutil
from typing import BinaryIO
from .adapter import FileStorageAdapter

class MockStorageAdapter:
    def __init__(self, base_dir: str = "packages/api/storage/wecom/"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    async def upload_file(self, file_path: str, content: BinaryIO) -> str:
        target_path = os.path.join(self.base_dir, os.path.basename(file_path))
        with open(target_path, "wb") as f:
            shutil.copyfileobj(content, f)
        return target_path

    async def download_file(self, file_id: str) -> bytes:
        if os.path.exists(file_id):
            with open(file_id, "rb") as f:
                return f.read()
        raise FileNotFoundError(f"File {file_id} not found")

    async def get_url(self, file_id: str) -> str:
        return f"file://{os.path.abspath(file_id)}"
