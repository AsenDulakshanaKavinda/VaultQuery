'''
This module defines the data models and validation rules for user context and group names in the data onboarding domain. 
It uses Pydantic for data validation and type enforcement, ensuring that user IDs, organization IDs, 
and group names adhere to specified constraints. The UserContext model is immutable, 
meaning its attributes cannot be modified after creation, which helps maintain data integrity.
'''

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from data_onboarding.domain.documents import SourceSystem

GROUP_PATTERN = r"^grp_[a-z0-9_]+$"
HINT_PATH = "path"
HINT_CHANNEL = "channel_name"
HINT_PROJECT = "project_key"


# allow attach metadata and validation rules
# remove whitespace and Enforces a regular expression patter for group name
GroupName = Annotated[str, StringConstraints(strip_whitespace=True, pattern=GROUP_PATTERN)]

def normalize_groups(groups: list[str]) -> list[str]:
    '''De-duplicate and sort so the same ACL always serializes the same way.'''
    return sorted(set(groups))


class UserContext(BaseModel):
    '''
    model_config make model immutable (read-only)
    can't modify after create
    user_id, org_id and groups can't be empty
    groups must have valid pattern
    '''
    model_config = ConfigDict(frozen=True)
    user_id: str = Field(min_length=1)
    org_id: str = Field(min_length=1)
    groups: frozenset[GroupName] = Field(min_length=1)

    @field_validator("groups")
    @classmethod
    def _not_empty(cls, v: frozenset[str]) -> frozenset[str]:
        if not v:
            raise ValueError("a user must hold at least one group")
        return v

class PathPrefixMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: Literal["path_prefix"]
    value: str = Field(min_length=1)

class ChannelNameMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: Literal[""]
    value: str = Field(min_length=1)

class ProjectKeyMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: Literal["project_key"]
    value: list[str] = Field(min_length=1)

Match = Annotated[PathPrefixMatch | ChannelNameMatch | ProjectKeyMatch, Field(discriminator="type")]

class AclRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str = Field(max_length=1)
    source_system: SourceSystem
    match: Match
    allowed_groups: list[GroupName] = Field(min_length=1)
    confidentiality: str | None = None
    content_type: str | None = None

class AclMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int
    rules: list[AclRule]

class Group(BaseModel):
    model_config = ConfigDict(extra="forbid")
    level: int
    label: str
    inherits: list[str] = Field(default_factory=list)

class GroupHierarchy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["explicit", "inherit"] = "explicit"
    always_granted: list[str]
    groups: dict[str, Group]
    role_claim_to_group: dict[str, str]









