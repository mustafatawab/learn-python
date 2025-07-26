from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel

# 100 = Information
# 200 = Success -> related to the request
# 300 = Redirect -> related to the request
# 400 = Client Error -> related to  the request
# 500 = Server Error -> related to the server

class User(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    user_id: int
    status: str

app = FastAPI()

@app.get("/info/{username}/{user_id}") # Path Parameters
def get_info(
            username: str = Path(... , min_length=3 , max_length=20),
            user_id: int = Path(..., gt=0, lt=100)
            ):

    if username == "test":
        raise HTTPException(status_code=404, detail=f"User {username} not found")

    return { "username" : username, "user_id" : user_id }


@app.get("/users/all")
def get_all_users(limit: int | None = Query(..., gt=0, lt=150)): # Query Paramters
    print(limit)
    if limit:
        return { "name" : "Mustafa Tawab"}
        
    return { 
        "user" : 
            [ 
                {"name" : "Mustafa Tawab"}, 
                { "name" : "Jamal"} 
            ]                    
    }   
    

@app.get("/product/{product_name}")
def product_details(
        product_name: str = Path(..., min_length=2, max_length=30),
        id: int = Query(...,gt=0, lt=100)):
    return {
        "product_nsame" : product_name,
        "ID" : id
    }


# To pass the data in the body you need to define a class inherited from the BaseModel and FastAPI will automatic recognize it.
@app.post("/create-user" , response_model=UserResponse)  
def create_user(user: User, user_id: int):
    return { "status" : "User Created" , "user_id" : user_id}



@app.put("/update-user/{user_id}")
def update_user(user: User , user_id: int = Path(...,gt=0,lt=100) ):
    print("\n [USER] " , user)
    return { "user_id": user_id, "status": "User Updated", "user" : user}



@app.patch("/update-user-partial/{user_id}")
def update_user_partial(user: User , user_id: int = Path(...,gt=0,lt=100)):
    print("\n [USER] " , user)
    return { "user_id": user_id, "status": "User Updated"}



@app.delete("/delete-user/{user_id}")
def delete_user(user: User, user_id: int = Path(...,gt=0,lt=100) ):
    return { "user_id": usre_id, "status": "User Deleted !"}