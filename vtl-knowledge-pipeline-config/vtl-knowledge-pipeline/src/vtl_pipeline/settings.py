"""Loads and validates all configuration at startup.

Secrets come from environment variables (.env, prefix VTL_).
Tunables come from config/settings.yaml. ACL policy comes from the two ACL yaml files.
Bad config should fail loudly here, not silently at 2 a.m. during an ingest run.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


# ---------- secrets (environment) ----------
class Secrets(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", env_prefix="VTL_", extra="ignore")

    env: Literal["local", "staging", "prod"] = "local"
    log_level: str = "INFO"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    postgres_dsn: str
    amqp_url: str

    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_region: str = "us-east-1"

    slack_bot_token: str | None = None
    slack_signing_secret: str | None = None
    jira_base_url: str | None = None
    jira_email: str | None = None
    jira_api_token: str | None = None
    jira_webhook_secret: str | None = None
    ms_tenant_id: str | None = None
    ms_client_id: str | None = None
    ms_client_secret: str | None = None

    embedding_api_key: str | None = None
    jwt_issuer: str | None = None
    jwt_audience: str | None = None
    jwt_jwks_url: str | None = None


# ---------- tunables (settings.yaml) ----------
class Chunking(BaseModel):
    chunk_size_tokens: int = Field(512, gt=0)
    chunk_overlap_tokens: int = Field(64, ge=0)
    chunker_version: str = "1"

    @model_validator(mode="after")
    def _overlap_smaller_than_chunk(self) -> Chunking:
        if self.chunk_overlap_tokens >= self.chunk_size_tokens:
            raise ValueError("chunk_overlap_tokens must be smaller than chunk_size_tokens")
        return self


class Embedding(BaseModel):
    provider: str
    model: str
    dimensions: int = Field(gt=0)
    batch_size: int = 64


class VectorStore(BaseModel):
    collection: str
    distance: Literal["Cosine", "Dot", "Euclid"] = "Cosine"
    indexed_payload_fields: list[str]


class PipelineCfg(BaseModel):
    batch_size: int = 100
    max_retries: int = 5
    retry_backoff_seconds: int = 2
    dead_letter_after_failures: int = 5
    skip_unchanged: bool = True
    tombstone_deletes: bool = True


class AclCfg(BaseModel):
    mapping_file: Path
    hierarchy_file: Path
    quarantine_group: str = "grp_quarantine"
    fail_on_unmapped: bool = False


class AppConfig(BaseModel):
    org_id: str
    chunking: Chunking
    embedding: Embedding
    vector_store: VectorStore
    pipeline: PipelineCfg
    acl: AclCfg
    s3: dict
    sharepoint: dict
    slack: dict
    jira: dict
    api: dict


# ---------- ACL policy ----------
class Group(BaseModel):
    level: int
    label: str
    inherits: list[str] = []


class GroupHierarchy(BaseModel):
    mode: Literal["explicit", "inherit"] = "explicit"
    always_granted: list[str]
    groups: dict[str, Group]
    role_claim_to_group: dict[str, str]

    def resolve_user_groups(self, own_group: str) -> set[str]:
        """Groups a logged-in user holds, used to build the pre-retrieval filter."""
        held = {own_group, *self.always_granted}
        if self.mode == "inherit":
            stack = [own_group]
            while stack:
                for g in self.groups[stack.pop()].inherits:
                    if g not in held:
                        held.add(g)
                        stack.append(g)
        return held


class AclRule(BaseModel):
    id: str
    source_system: Literal["s3", "sharepoint", "slack", "jira"]
    match: dict
    allowed_groups: list[str] = Field(min_length=1)  # never empty
    confidentiality: str | None = None
    content_type: str | None = None


class AclMapping(BaseModel):
    version: int
    rules: list[AclRule]


class Settings(BaseModel):
    secrets: Secrets
    app: AppConfig
    hierarchy: GroupHierarchy
    acl_mapping: AclMapping

    @model_validator(mode="after")
    def _all_rule_groups_exist(self) -> Settings:
        known = set(self.hierarchy.groups)
        for rule in self.acl_mapping.rules:
            unknown = set(rule.allowed_groups) - known
            if unknown:
                raise ValueError(f"ACL rule '{rule.id}' uses unknown groups: {sorted(unknown)}")
        if self.app.acl.quarantine_group not in known:
            raise ValueError("quarantine_group must be defined in group_hierarchy.yaml")
        return self


def _yaml(path: Path) -> dict:
    return yaml.safe_load((path if path.is_absolute() else ROOT / path).read_text())


@lru_cache
def get_settings() -> Settings:
    app = AppConfig(**_yaml(ROOT / "config" / "settings.yaml"))
    return Settings(
        secrets=Secrets(),  # type: ignore[call-arg]  # required fields come from env
        app=app,
        hierarchy=GroupHierarchy(**_yaml(app.acl.hierarchy_file)),
        acl_mapping=AclMapping(**_yaml(app.acl.mapping_file)),
    )
