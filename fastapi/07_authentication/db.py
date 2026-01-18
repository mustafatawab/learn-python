from sqlmodel import SQLModel,create_engine, Session
from fastapi import FastAPI
# from core.config import get_settings
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv


# settings = get_settings()

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print("Database Url =  " , database_url)
engine = create_engine(database_url , echo=True)

async def get_session():
    with Session(engine) as session:
        yield session


