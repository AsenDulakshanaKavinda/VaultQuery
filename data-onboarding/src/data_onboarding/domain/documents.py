import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

from data_onboarding.domain.ids import content_hash, make_doc_id

SourceSystem = Literal["s3", "sharepoint", "slack", "jira"]

class SourceDocument(BaseModel):
    """
    what every connector should return from fetch() and what the pipeline will store in the db
    """

    model_config = ConfigDict(frozen=True)
    org_id: str = Field(min_length=1)
    source_system: SourceSystem
    source_id: str = Field(min_length=1)
    title: str | None = None
    content: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    acl_hints: dict[str, Any]
    updated_at: datetime

    @computed_field
    @property
    def doc_id(self) -> str:
        ''' 
        this method is used to generate a unique document id for the document, 
        based on the org_id, source_system, and source_id. use computed_field 
        to ensure that the doc_id is always up-to-date with the other fields. 
        '''
        return make_doc_id(self.org_id, self.source_system, self.source_id)

    @computed_field  
    @property
    def content_hash(self) -> str:
        '''
        this method is used to compute a SHA-256 hash of the document's content, 
        which can be used to uniquely identify the content of the document. 
        use computed_field to ensure that the content_hash is always up-to-date with the content field. 
        '''
        return content_hash(self.content)
    