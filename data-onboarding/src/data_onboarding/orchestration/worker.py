

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from data_onboarding.orchestration.workflows import SmartSyncWorkflow
from data_onboarding.orchestration.activities import (
    list_source_changes_activity,
    process_single_document_activity,
    handle_deletions_activity,
)
from data_onboarding.observability import log

async def main():
    client = await Client.connect("localhost:7233")
    
    worker = Worker(
        client,
        task_queue="vtl-pipeline-queue",
        workflows=[SmartSyncWorkflow],
        activities=[
            list_source_changes_activity,
            process_single_document_activity,
            handle_deletions_activity,
        ],
    )
    
    log.info("Starting VTL Temporal Ingestion Worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())