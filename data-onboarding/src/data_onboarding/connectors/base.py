

from collections.abc import AsyncIterable
from datetime import datetime
from typing import Any, Protocol


class BaseConnector(Protocol):
    """ abstract interface for all source connectors """
    
    async def list_changes(self, since: datetime | None = None) -> AsyncIterable[str]:
        """ Yield source item IDs or paths that have changed or need syncing."""
        ...

    async def fetch(self, source_id: str) -> tuple[bytes, dict[str, Any]]:
        """ Download raw binary content and metadata hints (e.g. {"path": ...}). """
        ...


    async def list_acl(self, source_id: str) -> dict[str, Any]:
        """ Return raw ACL hints/metadata for mapping """









