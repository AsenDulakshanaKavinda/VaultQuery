import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy


@workflow.defn
class SmartSyncWorkflow:
    @workflow.run
    async def run(self, source_system: str, poll_interval_seconds: int = 10) -> None:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(minutes=1),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )
        while True:
            # 1. List changes via activity string name
            live_source_ids = await workflow.execute_activity(
                "list_source_changes_activity",
                source_system,
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy,
            )

        

            # 2. Process documents concurrently by passing arguments as a single tuple
            processing_futures = [
                workflow.execute_activity(
                    "process_single_document_activity",
                    (source_system, source_id),  # Bundled into a single tuple argument
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=retry_policy,
                )
                for source_id in live_source_ids
            ]

            if processing_futures:
                await asyncio.gather(*processing_futures)

            # 3. Handle deletions via activity string name (bundled tuple argument)
            purged_count = await workflow.execute_activity(
                "handle_deletions_activity",
                (source_system, live_source_ids),
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy,
            )

            # return {"source_system": source_system,"total_processed": len(live_source_ids),"purged_tombstones": purged_count,"status": "completed",}
            await workflow.sleep(timedelta(seconds=poll_interval_seconds))