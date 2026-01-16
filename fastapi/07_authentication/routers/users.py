from fastapi import APIRouter, Depends
from models.user import User
from schema.user import UserCreate, UserLogin
from db import get_session
from sqlmodel import Session

router = APIRouter(
    prefix="/auth",
    tags=["users"]
)


@router.get("/")
async def user_health_check():
    return {"Status" : "All Good"}


# @router.post("/signup")
# async def register_user()
