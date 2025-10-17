from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine, select
from models import Item
from contextlib import asynccontextmanager


DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_DHQNy1KACE5w@ep-little-sound-afysg28k-pooler.c-2.us-west-2.aws.neon.tech/ecom?sslmode=require&channel_binding=require"
engine = create_engine(DATABASE_URL , echo=True)

def get_session():
    with Session(engine) as session:
        yield session

        
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables...")
    SQLModel.metadata.create_all(engine)
    yield
    print("Shutting down")

