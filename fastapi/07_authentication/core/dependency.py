from sqlmodel import SQLModel, select, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User as UserTable
from core.security import hash_password, decode_token, create_access_token
from core.config import get_settings
from db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")
print("OAuth 2 Scheme  =  " , oauth2_scheme)

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )

    payload =  decode_token(token)
    print("Payload = " , payload)
    if not payload:
        print("\Payload is None")
        raise credential_exception

    username: str = payload.get("username")

    user = session.exec(select(UserTable).where(UserTable.username == username)).first()

    if not user:
        print("\nUser is None")
        raise credential_exception
    
    return user
