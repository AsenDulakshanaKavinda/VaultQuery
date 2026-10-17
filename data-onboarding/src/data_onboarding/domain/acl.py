"""
This module defines the data models and validation rules for user context and group names in the data onboarding domain. 
It uses Pydantic for data validation and type enforcement, ensuring that user IDs, organization IDs, 
and group names adhere to specified constraints. The UserContext model is immutable, 
meaning its attributes cannot be modified after creation, which helps maintain data integrity.
"""

from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints


# allow attach metadata and validation rules
# remove whitespace and Enforces a regular expression patter for group name
GroupName = Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^grp_[a-z0-9_]+$")]

def normalize_groups(groups: list[str]) -> list[str]:
    """De-duplicate and sort so the same ACL always serializes the same way."""
    return sorted(set(groups))

# model_config make model immutable (read-only)
# can't modify after create
# user_id, org_id and groups can't be empty
# groups must have valid pattern
class UserContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    user_id: str = Field(min_length=1)
    org_id: str = Field(min_length=1)
    groups: frozenset[GroupName] = Field(min_length=1)