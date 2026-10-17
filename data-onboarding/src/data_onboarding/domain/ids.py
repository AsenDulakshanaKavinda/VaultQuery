
"""
THis module provides functions to generate unique identifiers for documents and chunks within a data onboarding context.

NAMESPACE - fixes and generated once
SEP - ASCII unit separator

_check - helper function to validate input values
make_doc_id - generates a unique document ID based on org_id, source_system, and source_id
make_chunk_id - generates a unique chunk ID based on doc_id and chunk_index

1. uuid5, not a random UUID or Python’s hash(). uuid5 is a pure function of its input, 
    so re-running ingestion overwrites the same Qdrant points instead of duplicating them. It’s also a valid Qdrant point ID.
2. The key includes org_id. Two tenants with the same Slack channel ID must never collide.
3. The separator is \x1f, not :. With a : join, ("a:b", "c") and ("a", "b:c") produce the same key.
4. No lowercasing. Slack, Jira and S3 IDs are case-sensitive, so normalizing them would merge distinct documents.
"""

import uuid

NAMESPACE = uuid.UUID("99e62a8c-e042-46da-94fc-c1e1902750a2")
SEP = "\x1f"

def _check(name: str, value: str) -> str:
    """ 
    reject empty or whitespace-only values
    reject values containing the separator
    return value
    """
    if not value or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    if SEP in value:
        raise ValueError(f"{name} must not contain the separator character")
    return value # deliberately NOT lowercased: Slack/Jira/S3 IDs are case-sensitive

def make_doc_id(org_id, source_system, source_id) -> str:
    """
    This function generates a unique document ID based on the organization ID, source system, and source ID. 
    It uses a namespace UUID and a separator to create a key, 
    which is then hashed using UUID version 5 to produce a consistent and unique identifier.
    """
    key = SEP.join((_check("org_id", org_id), _check("source_system", source_system), _check("source_id", source_id)))
    return str(uuid.uuid5(NAMESPACE, key))

def make_chunk_id(doc_id, chunk_index) -> str:
    """
    This function generates a unique chunk ID based on the document ID and chunk index. 
    It uses a namespace UUID and a separator to create a key, 
    which is then hashed using UUID version 5 to produce a consistent and unique identifier.
    """
    return str(uuid.uuid5(NAMESPACE, SEP.join((_check("doc_id", doc_id), str(chunk_index)))))