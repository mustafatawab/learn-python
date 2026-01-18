from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username : str
    password : str


class UserReponse(BaseModel):
    id: int
    username: str
    email: str

  