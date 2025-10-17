from fastapi import FastAPI
from database import lifespan
from routers import items

app = FastAPI(lifespan=lifespan)
app.include_router(items.router)
