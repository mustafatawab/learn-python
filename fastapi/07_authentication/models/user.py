from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int | None = Field(default=True, primary_key=True, index=True)
    username: str = Field(min_length=5, unique=True)
    email: EmailStr
    password : str = Field(min_length=8)

