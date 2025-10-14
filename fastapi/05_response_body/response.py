from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

class Item(BaseModel):
    name : str
    price : float
    description: Optional[str] = None
    is_offer: Optional[bool] = None
    owner: Optional[User] = None
    

route = FastAPI()

@route.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]




@route.get("/items/{item_id}" , response_model=Item)
async def get_single_item(item_id : int):
    print("Item ID  ", item_id )
    return {
        "name": "Item 1",
        "price": 10.5,
        "description": "This is item 1",
        "is_offer": False,
        "owner": {
            "username": "johndoe",
            "full_name": "John Doe"
        }
    }


@route.post("/items/", response_model=Item , response_model_exclude={"description", "is_offer"})
async def create_item(item: Item):
    print("Item Added  ", item )
    return item

@route.post("/items2/", response_model=Item , response_model_include={"name", "price"})
async def create_item2(item: Item):
    print("Item Added  ", item )
    return item