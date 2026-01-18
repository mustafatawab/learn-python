from fastapi import APIRouter, HTTPException,status, Depends
from models.user import User as UserTable
from schema.user import UserCreate, UserLogin, UserReponse
from db import get_session
from sqlmodel import Session,select
from core.security import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")
print("OAuth 2 Scheme  =  " , oauth2_scheme)

router = APIRouter(
    prefix="/auth",
    tags=["users"]
)




async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )

    payload = decode_token(token)
    if payload is None:
        raise credential_exception

    username: str = payload.get("username")

    user = session.exec(select(UserTable).where(UserTable.username == username)).first()

    if user is None:
        raise credential_exception
    
    return user



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
async def signin(user: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    check_user = session.exec(select(UserTable).where(UserTable.username == user.username)).first()
    if check_user:
        check_password = verify_password(user.password , check_user.password)
        if check_password:
            token = create_access_token({"username" : user.username})
            return {"token_type" : "bearer" , "token" : token}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exists")



@router.get("/users/me")
async def read_current_user(current_user : UserTable = Depends(get_current_user)):
    return {"id" : current_user.id , "username" : current_user.username}