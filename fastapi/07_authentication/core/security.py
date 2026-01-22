from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from core.config import get_settings

settings = get_settings()

password_hash = PasswordHash((Argon2Hasher(),))



def hash_password(password):
    """ Hash the password """
    return password_hash.hash(password=password)



def verify_password(plain_password: str , hash_password) -> bool:
    """ Verify Password  """
    return password_hash.verify(plain_password, hash_password)


def create_access_token(data: dict) -> str:
    """ Create access token for the authenticion - JWT Token """
    
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=20)
    to_encode.update({"exp" : expire_time})
    token = jwt.encode(to_encode, settings.jwt_secret , settings.algorithm)

    return token



def decode_token(token: str) -> dict | None:
    """ Decode Token """

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=settings.algorithm) 
        return  payload
    except JWTError as error:
        print("Error is " , error)
        return None