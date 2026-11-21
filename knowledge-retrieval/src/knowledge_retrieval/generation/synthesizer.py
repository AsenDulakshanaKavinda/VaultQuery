


from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from knowledge_retrieval.generation.prompt_loader import render_prompt
from knowledge_retrieval.generation.tools import search_documents
load_dotenv()

@asynccontextmanager
async def agent_lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(os.environ["DATABASE_URL"]) as checkpointer:
        await checkpointer.setup()
        app.state.agent = create_agent(
            model=ChatGroq(model="openai/gpt-oss-20b", temperature=0), 
            tools=[search_documents],
            system_prompt=render_prompt("system_qa.jinja2", {}),
            checkpointer=checkpointer,
        )
        yield











