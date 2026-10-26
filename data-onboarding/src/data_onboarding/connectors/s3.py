from collections.abc import AsyncIterable
from datetime import datetime
from typing import Any

from minio import Minio

from data_onboarding.connectors.base import BaseConnector
from data_onboarding.core import get_settings
from data_onboarding.observability import log

settings = get_settings()


class MinIOClient:
    """A singleton client for interacting with MinIO"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.client = Minio(
                endpoint=settings.secrets.minio_endpoint,
                access_key=settings.secrets.minio_access_key,
                secret_key=settings.secrets.minio_secret_key,
                secure=False, #settings.secrets.minio_secure,
            )

            log.info("MinIO Client initialized")
        return cls._instance


def get_minio_client() -> Minio:
    instance = MinIOClient()
    if instance is None:
        raise RuntimeError("MinIOClient instance is None. Check environment variables or initialization logic.")
    return instance.client


class S3Connector(BaseConnector):
    def __init__(self, bucket_name: str, allowed_extension: tuple[str, ...] = (".pdf", ".docx")):
        self.client = get_minio_client()
        self.bucket_name = bucket_name
        self.allowed_extension = allowed_extension

    async def list_changes(self, since: datetime | None = None) -> AsyncIterable[str]:
        ''' Yield source item IDs or paths that have changed or need syncing. '''
        # *note: use AsyncIterable, and yield - can use with async for loop (this is for memory efficiency)

        objects = self.client.list_objects(self.bucket_name, recursive=True)
        for obj in objects:
            if obj.object_name.endswith(self.allowed_extension):
                yield obj.object_name

    async def fetch(self, source_id: str) -> tuple[bytes, dict[str, Any]]:
        ''' Download raw binary content and metadata hints (e.g. {"path": ...}). '''
        response = self.client.get_object(self.bucket_name, source_id)
        data = response.read()
        response.close()
        response.release_conn()

        hints = {"path": f"/{self.bucket_name}/{source_id}"}
        return data, hints


    async def list_acl(self, source_id: str) -> dict[str, Any]:
        ''' Return raw ACL hints/metadata for mapping '''
        return {"path": f"/{self.bucket_name}/{source_id}"}






