from sqlmodel import SQLModel , Field , create_engine, Session, select
import settings
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
import os
from contextlib import asynccontextmanager


# from dotenv import load_dotenv, find_dotenv
# _: bool = load_dotenv(find_dotenv())

# DATABASE_URL = os.environ.get('DATABASE_URL')
# if not DATABASE_URL:
#     raise ValueError("Please set the database url correctly !!")


# Models (Table Model , Data Model)
class Todo(SQLModel, table=True):
    id : int | None = Field(default=None , primary_key=True)
    content: str = Field(index=True, min_length=5 , max_length=60)
    is_completed: bool = Field(default=False)


# Psycopg is a driver that communicate with the database. 
# Engine is one for the whole app
connection_string = str(settings.DATABASE_URL).replace("postgresql" , "postgresql+psycopg")
engine = create_engine(connection_string , connect_args={"sslmode" : "require"} , pool_recycle=300 , pool_size=10 , echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


# todo1 : Todo = Todo(content='First Task')

# # Session is for each task or each functionality/transaction
# session = Session(engine) # Session will use our engine to create session

# # Create Todos in database
# session.add(todo1)
# session.commit()
# session.close()


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    yield


app: FastAPI = FastAPI(lifespan=lifespan, title="Todo App" , version='1.0')

@app.get('/')
def home():
    return {"message" : "Todo App"}



@app.post("/todos" , response_model=Todo)
async def create_todo(todo: Todo , session: Annotated[Session,Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todos", response_model=list[Todo])
async def get_all_todos(session: Annotated[Session, Depends(get_session)]):
    # statement = select(Todo)
    todos = session.exec(select(Todo)).all()
    if todos:
        return todos
    else:
        raise HTTPException(status_code=404, detail="No Task Found")


@app.get("/todos/{id}" , response_model=Todo)
async def get_single_todo(id: int, session: Annotated[Session, Depends(get_session)]):
    # select(Todo).where(Todo.id == id)
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail='No Task Found')


@app.put('/todos/{id}' , response_model=Todo)
async def edit_todo(id: int , todo: Todo , session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.exect(select(Todo).where(Todo.id == id)).first()
    if existing_todo:
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed

        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)

        return existing_todo
    else:
        raise HTTPException(status_code=404, detail='No Task Found')


@app.delete('/todos/{id}')
async def delete_todo(id: int , session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    #  todo = session.get(Todo , id)
    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)
        return {
            "message" : "Task Deleted Successfully !!!"
        }
    else:
        raise HTTPException(status_code=404, detail='Todo not found')