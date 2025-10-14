from fastapi import FastAPI 
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name : str
    price : float
    description: Optional[str] = None


items_db: list[Item] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item


@app.get("/items/" , response_model=list[Item])
async def get_all_items():
    return items_db


@app.get("/items/{item_id}" , response_model=Item)
async def get_single_item(item_id : int):
    return items_db[item_id]


@app.put("/items/{item_id}" , response_model=Item)
async def update_item(item_id : int , item: Item):
    items_db[item_id] = item
    return item


@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id : int):
    items_db.pop(item_id)
    return {"message": "Item deleted successfully."}