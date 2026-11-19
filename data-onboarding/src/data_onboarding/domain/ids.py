import uuid

NAMESPACE = uuid.UUID("6f1d2b0e-3c53-4f0b-9a57-5f3a9c0d7e11")  # fixed, generated once
SEP = "\x1f"  # ASCII unit separator


def _check(name: str, value: str) -> str:
    if not value or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    if SEP in value:
        raise ValueError(f"{name} must not contain the separator character")
    return value  # deliberately NOT lowercased: Slack/Jira/S3 IDs are case-sensitive


def make_doc_id(org_id, source_system, source_id) -> str:
    key = SEP.join(
        (
            _check("org_id", org_id),
            _check("source_system", source_system),
            _check("source_id", source_id),
        )
    )
    return str(uuid.uuid5(NAMESPACE, key))


def make_chunk_id(doc_id, chunk_index) -> str:
    return str(
        uuid.uuid5(NAMESPACE, SEP.join((_check("doc_id", doc_id), str(chunk_index))))
    )
