from __future__ import annotations
from functools import lru_cache
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

ROOT = ""

class Secrets(BaseSettings):
    model_config = SettingsConfigDict(env_file="", env_prefix=None, extra=None)
    
    env: Literal["local", "staging", "prod"]
    log_level: str = "INFO"

    minio_endpoint: str | None = None
    minio_access_key: str | None = None
    minio_secret_key: str | None = None
    minio_secure: str | None = None

class AppConfig(BaseModel):
    name: str

class Settings(BaseModel):
    secrets: Secrets
    app: AppConfig

def _yaml(path: Path) -> dict:
    return yaml.safe_load(
        (path if path.is_absolute() else ROOT / path).read_text()
    )

@lru_cache
def get_settings() -> Settings:
    app = AppConfig(**_yaml(ROOT / "config" / "settings.yaml"))
    return Settings(
        secrets=Secrets(),
        app=app
    )
