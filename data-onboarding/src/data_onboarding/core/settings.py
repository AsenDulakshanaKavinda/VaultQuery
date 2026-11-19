from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent.parent.parent


class Secrets(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: Literal["local", "staging", "prod"]
    log_level: str = "INFO"

    minio_endpoint: str | None = None
    minio_access_key: str | None = None
    minio_secret_key: str | None = None
    minio_secure: str | None = None
    minio_bucket: str | None = None

    sharepoint_site_url: str | None = None
    sharepoint_tenant_name: str | None = None
    sharepoint_client_id: str | None = None
    sharepoint_client_secret: str | None = None

    jira_server: str | None = None
    jira_basic_auth: str | None = None
    jira_token_auth: str | None = None

    slack_token: str | None = None

    hf_token_read: str | None = None

    qdrant_url: str | None = None

    async_database_url: str | None = None

    s3_bucket_name: str | None = None




class AppConfig(BaseModel):
    name: str


class Settings(BaseModel):
    secrets: Secrets
    app: AppConfig


def _yaml(path: Path) -> dict:
    return yaml.safe_load((path if path.is_absolute() else ROOT / path).read_text())


@lru_cache
def get_settings() -> Settings:
    """
    Loads settings from the .env file and the settings.yaml file.
    use lru_cache to cache the settings so that they are only loaded once.
    """
    app = AppConfig(**_yaml(ROOT / "config" / "settings.yaml"))
    return Settings(secrets=Secrets(), app=app)

from pathlib import Path

