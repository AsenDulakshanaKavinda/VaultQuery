


from temporalio import activity

from data_onboarding.connectors.base import BaseConnector



@activity.defn
async def list_source_changes_activity(source_system: str) -> list[str]:
    """ """
    connector: BaseConnector = BaseConnector()

    source_ids = []
    async for source_id in connector.list_changes():
        source_ids.append(source_id)
    return source_ids


@activity.defn
async def process_single_document_activity(source_system: str, source_id: str) -> str:
    


