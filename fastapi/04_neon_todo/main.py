from sqlmodel import SQLModel , Field , create_engine
import settings
from fastapi import FastAPI


class Todo(SQLModel):
    id : int | None = Field(default=None , primary_key=True)
    content: str = Field(index=True, min_length=5 , max_length=60)
    is_completed: bool = Field(default=False)

connection_string = str(settings.DATABASE_URL).replace("postgresql" , "postgresql+psycopg")
engine = create_engine(connection_string , connect_args={"sslmode" : "require"} , pool_recycle=300)


app: FastAPI = FastAPI()