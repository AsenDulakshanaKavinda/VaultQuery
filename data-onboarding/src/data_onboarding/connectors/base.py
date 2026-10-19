


from collections.abc import Iterator
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from data_onboarding.domain.documents import SourceDocument, SourceSystem


class SourceObjectNotFound(Exception):
    ''' 
    fetch() raise this when the object no longer exists in the source
    the pipeline threats it like a delete, so a race between list_changes() and
    fetch() dose not crash a run
    '''

class Change(BaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["upsert", "delete"]
    source_id: str = Field(min_length=1)
    cursor: str | None = None

class ACLEntry(BaseModel):
    model_config = ConfigDict(frozen=True)
    source_id: str = Field(min_length=1)
    acl_hints: dict[str, Any]
    
@runtime_checkable
class Connector(Protocol):
    source_system: SourceSystem


    def list_changes(self, since: str | None = None) -> Iterator[Change]:
        ''' list all changes since the given cursor, or all changes if since is None '''
        ...


    def fetch(self, source_id: str) -> SourceDocument:
        ''' download and retune one object as a SourceDocument '''
        ...

    def list_acl(self) -> Iterator[ACLEntry]:
        ''' list all ACLs for the source system '''
        ... 
        



