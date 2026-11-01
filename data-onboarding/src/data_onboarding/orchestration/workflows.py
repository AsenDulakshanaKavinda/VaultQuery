

from temporalio import workflow
from temporalio.common import RetryPolicy



@workflow.defn
class IngestDocumentWorkflow:
    @workflow.run
    async def run(self, source_system: str, source_id: str) -> str:
        ...










