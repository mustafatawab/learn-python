from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price : int
    description : Optional[str] = None

class ItemCreate(BaseModel):
    name: str
    price : int
    description : Optional[str] = None