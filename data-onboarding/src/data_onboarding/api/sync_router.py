

from fastapi import APIRouter, Depends, HTTPException, Request
from temporalio.client import Client

router = APIRouter(prefix="/api/v1/sync", tags=["Orchestration"])


def get_temporal_client(request: Request) -> Client:
    """Dependency to extract the Temporal client stored in FastAPI app state."""
    return request.app.state.temporal_client


@router.post("/trigger/{source_system}")
async def trigger_sync(
    source_system: str, 
    temporal_client: Client = Depends(get_temporal_client)
):
    """Kicks off a durable Temporal sync workflow for S3, SharePoint, etc."""
    try:
        handle = await temporal_client.start_workflow(
            "SmartSyncWorkflow",  # Or your workflow class name
            source_system,
            id=f"smart-sync-{source_system}",
            task_queue="vtl-pipeline-queue",
        )
        return {
            "workflow_id": handle.id, 
            "run_id": handle.result_run_id, 
            "status": "started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))