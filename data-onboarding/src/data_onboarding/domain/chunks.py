

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from data_onboarding.domain.acl import GroupName, normalize_groups
from data_onboarding.domain.documents import SourceSystem
from data_onboarding.domain.ids import make_chunk_id


class Chuck(BaseModel):
    model_config = ConfigDict(frozen=True)
    org_id: str; doc_id: str; chunk_index: int = Field(ge=0)
    source_system: SourceSystem; source_url: str
    test: str = Field(min_length=1); chunk_version: str
    allowed_groups: list[GroupName] = Field(min_length=1)

    @field_validator("allowed_groups")
    def _dedupe_sort(cls, v): return normalize_groups(v)

    @computed_field
    @property
    def chunk_id(self) -> str: return make_chunk_id(self.doc_id, self.chunk_index)