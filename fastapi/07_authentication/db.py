from sqlmodel import SQLModel,create_engine, Session
from fastapi import FastAPI
from core.config import get_settings
from contextlib import asynccontextmanager


settings = get_settings()


engine = create_engine(settings.database_url , echo=True)

async def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\nStarting App")
    print("\nCreating Tables")
    SQLModel.metadata.create_all(engine)
    yield
    print("\nShutting Down")

