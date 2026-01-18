from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=5, unique=True)
    email: EmailStr = Field(unique=True)
    password : str = Field(min_length=8)

