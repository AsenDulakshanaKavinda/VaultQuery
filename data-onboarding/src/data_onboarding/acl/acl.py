from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

# GroupName: ^grp_[a-z0-9_]+$
GroupName = Annotated[str, StringConstraints(pattern="^grp_[a-z0-9_]+$")]

# hint keys
HINT_PATH = "path"
HINT_CHANNEL = "channel_name"
HINT_PROJECT = "project_key"

SourceSystem = Literal["s3", "sharepoint", "slack", "jira"]


class PathPrefixMatch(BaseModel):
    """
    A model representing a path prefix match.
    used for sharepoint and s3,
    wraps a dir path string prefix
    """

    model_config = ConfigDict(frozen=True)
    type: Literal["path_prefix"] = "path_prefix"
    value: str  # e.g., "/SharePoint/Legal/Contracts/"


class ChannelNameMatch(BaseModel):
    """
    A model representing a channel name match.
    used for slack, contains a list of channel names to match against.
    """

    model_config = ConfigDict(frozen=True)
    type: Literal["channel_name"] = "channel_name"
    values: list[str]  # e.g., ["general", "announcements"]


class ProjectKeyMatch(BaseModel):
    """
    A model representing a project key match.
    used for jira, contains a list of project keys to match against.
    """

    model_config = ConfigDict(frozen=True)
    type: Literal["project_key"] = "project_key"
    values: list[str]  # e.g., ["IT", "WH"]


"""
The policy uses tagged union variants (AclMatch) to structure match rules depending on the source system:
- PathPrefixMatch: Used for sharepoint and s3. Wraps a directory path string prefix
    (e.g., "/SharePoint/Legal/Contracts/").
- ChannelNameMatch: Used for slack. Contains a list of channel names
    (e.g., ["general", "announcements"]).
- ProjectKeyMatch: Used for jira. Contains a list of project key identifiers
    (e.g., ["WH", "IT"]).
"""
AclMatch = PathPrefixMatch | ChannelNameMatch | ProjectKeyMatch


class AclRule(BaseModel):
    """
    maps a specific location match (PathPrefixMatch, ChannelNameMatch, ProjectKeyMatch)
    within a source system to a list of allowed security groups.
    allowed_groups can never by empty
    """

    model_config = ConfigDict(frozen=True)
    id: str
    source_system: SourceSystem
    match: AclMatch
    allowed_groups: list[GroupName]
    confidentiality: str | None = None
    content_type: str | None = None

    @model_validator(mode="after")
    def validate_allowed_groups_non_empty(self) -> "AclRule":
        if not self.allowed_groups:
            raise ValueError("allowed_groups must be non-empty")
        return self


class AclMapping(BaseModel):
    """
    Represents the loaded policy configuration from config/acl_mapping.yaml,
    containing a version string and an ordered list of AclRule objects
    (where rule order dictates priority).
    """

    model_config = ConfigDict(frozen=True)
    version: str
    rules: list[AclRule]


class Group(BaseModel):
    """Represents a security group with a level, label, and inheritance information."""

    model_config = ConfigDict(frozen=True)
    level: int
    label: str
    inherits: list[GroupName] = Field(default_factory=list)


class GroupHierarchy(BaseModel):
    """
    Represents the overall permission structure loaded from config/group_hierarchy.yaml.
    Stores evaluation mode (explicit vs. inherit), global groups (always_granted, e.g., ["grp_all"]),
    and mappings from authentication roles to base groups (role_claim_to_group).
    """

    model_config = ConfigDict(frozen=True)
    mode: Literal["explicit", "inherit"]
    always_granted: list[GroupName]
    groups: dict[GroupName, Group]
    role_claim_to_group: dict[str, GroupName]


class UserContext(BaseModel):
    """
    object created for an authenticated user query.
    Contains user_id, org_id, and a frozenset of resolved groups.
    Includes a validator ensuring no user context can be created with an empty group set.
    """

    model_config = ConfigDict(frozen=True)
    user_id: str
    org_id: str
    groups: frozenset[GroupName]

    @model_validator(mode="after")
    def validate_groups_non_empty(self) -> "UserContext":
        if not self.groups:
            raise ValueError("groups must be non-empty")
        return self


class SourceDocument(BaseModel):
    """Represents a source document with its system, path, and associated ACL hints."""

    model_config = ConfigDict(frozen=True)
    source_system: SourceSystem
    acl_hints: dict[str, Any]


class Chunk(BaseModel):
    """Represents a data chunk with its unique identifier and the set of allowed groups."""

    model_config = ConfigDict(frozen=True)

    org_id: str
    doc_id: str
    chunk_index: str
    source_system: str
    source_url: str
    text: str
    chunker_version: str
    allowed_groups: tuple[GroupName, ...]  # Non-empty, deduplicated, sorted
