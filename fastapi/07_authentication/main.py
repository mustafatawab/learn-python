from fastapi import FastAPI, Depends
from db import engine
from routers.users import router as user_router
from sqlmodel import SQLModel
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\nStarting App")
    print("\nCreating Tables")
    SQLModel.metadata.create_all(engine)
    yield
    print("\nShutting Down")




app = FastAPI(lifespan=lifespan,title="Todo App")



app.include_router(user_router)
