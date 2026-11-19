from temporalio import activity
from data_onboarding.orchestration.container import get_connector, get_smart_pipeline


@activity.defn
async def list_source_changes_activity(source_system: str) -> list[str]:
    connector = get_connector(source_system)
    source_ids = []
    async for source_id in connector.list_changes():
        source_ids.append(source_id)
    return source_ids


@activity.defn
async def process_single_document_activity(args: tuple[str, str]) -> str:
    source_system, source_id = args
    pipeline = get_smart_pipeline(source_system)
    await pipeline._process_single_item(source_id)
    return "SUCCESS"


@activity.defn
async def handle_deletions_activity(args: tuple[str, list[str]]) -> int:
    source_system, live_source_ids = args
    pipeline = get_smart_pipeline(source_system)
    await pipeline._handle_deletions(set(live_source_ids))
    return len(live_source_ids)