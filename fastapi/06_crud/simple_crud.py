from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()

class Users(BaseModel):
    id : int
    name: str
    email : str

class UsersCreate(BaseModel):
    name : str
    email : str


users_data: list[Users] = []

@app.post("/user", response_model=Users)
def create_user(user: UsersCreate):
    new_user = Users(id=len(users_data) + 1 , **user.model_dump())
    users_data.append(new_user)
    return new_user

@app.get("/users" , response_model=list[Users])
def get_users():
    return users_data

@app.get("/user/{user_id}" , response_model=Users)
def get_one_user(user_id: int):
    user = users_data[user_id]
    return user

@app.put("/user/{user_id}" , response_model=Users)
def update_user(user_id: int , user: UsersCreate):
    users_data[user_id] = user
    updated_user = user_id[user_id]
    return updated_user

@app.delete("/user/{user_id}" , response_model=Users)
def delete_user(user_id: int):
    deleted_user = user_id[user_id]
    users_data.pop(user_id)
    return delete_user

