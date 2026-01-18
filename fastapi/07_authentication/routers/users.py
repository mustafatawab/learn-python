from fastapi import APIRouter, HTTPException,status, Depends
from models.user import User as UserTable
from schema.user import UserCreate, UserLogin, UserReponse
from db import get_session
from sqlmodel import Session,select
from core.security import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["users"]
)


@router.get("/")
async def user_health_check():
    return {"Status" : "All Good"}


@router.post("/signup", response_model=UserReponse)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(UserTable).where(UserTable.email == user.email or UserTable.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email or username already exists")
    
    hashed_password = hash_password(user.password)

    add_user = UserTable(username=user.username, email=user.email, password=hashed_password)

    session.add(add_user)
    session.commit()
    session.refresh(add_user)
    return add_user



@router.post("/signin")
async def signin(user: UserLogin, session: Session = Depends(get_session)):
    check_user = session.exec(select(UserTable).where(UserTable.username == user.username)).first()
    if check_user:
        check_password = verify_password(user.password , check_user.password)
        if check_password:
            pass
