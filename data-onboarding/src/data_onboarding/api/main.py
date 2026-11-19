from contextlib import asynccontextmanager
from fastapi import FastAPI
from temporalio.client import Client
from data_onboarding.api.sync_router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Temporal server once
    app.state.temporal_client = await Client.connect("localhost:7233")
    yield
    # Shutdown: Clean up connections if needed


app = FastAPI(title="VTL Data Onboarding API", lifespan=lifespan)

# Include your routers here
app.include_router(router)