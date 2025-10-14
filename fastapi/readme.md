## FastAPI
- Backend framework based on Python. Easy to learn and build API with less code
- This is using swager ui
- Built in docs using swager ui


Install FastAPI in your UV Project or python file
``` uv add "fastapi[standard]" | pip install "fastapi[standard]" ```

Install Uvicorn
``` uv add uvicorn | pip install uvicorn```



```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message" : "Root"}


```



```python
from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/")
def read_root():
    return {"Message" : "Hello World"}

```
Run the server
```uv run uvicorn main:app --reload```
```uv run fastapi dev main.py --reload```




**Path Paremter** : 
It is part of the structure url. 
`/users/7` → the `7` is a path parameter (`user_id`).

**Query Parameters** : 
Comes after the `?` in the url, like filters or options
`/users?active=true&limit=10`


```python
@app.get("/users/{user_id}")
def read_user(user_id: int , q : str | None = None ):
    return {"user_id": user_id , "q" : q}
```


Q: What do you think will happen if you open /users/abc instead of /users/123?
A : FastAPI actually won’t return a JSON response like that. Instead, it’ll respond with an error, something like because of **pydantic** validation:
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "user_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}

```



![alt text](image.png)




### Response Body Model and Response Model


```python

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float

class ReponseItem(BaseModel):
    data : Item
    message : str

# The response_model parameter is used to specify the model that should be used to serialize the response.
@app.post("/" , response_model=ReponseItem)
def create_item(item: Item):
    """ Add Items """
    print(item)
    return {"data" : item , "message" : "Item Created Successfully"}



```


When adding extra field in the response (return of the function), the fastapi will ignore
```python

class Item(BaseModel):
    name : str
    price : int
    description: str


@app.get("/test" , response_model=Item)
def test():
    return {"name" : "perfume" , "price" : 200 , "description" : "This is long lasting perfume" , "extra" : "This is extra field"}
```
in the above the fast will ignore the extra field. 

**Why this is useful?**
- It prevents leaking sensitive data (like passwords , Internal IDs)
- It keep reponse consistant for the client
- It separates internal logic (your database models) from public contracts (your API schemas).


FastAPI also lets you control what fields to include or exclude with `response_model_include` and `response_model_exclude`.

```python 
@app.get("/items/{item_id}", response_model=Item, response_model_include={"name", "price"})
async def read_item(item_id: int):
    return {"name": "Laptop", "price": 1200.5, "is_offer": True, "description": "A gaming laptop"}

```
Response Would Be
```json
    {
    "name": "Laptop",
    "price": 1200.5
    }
```

If you want to exclude something

```python
@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"description"})
async def read_item(item_id: int):
    return {"name": "Laptop", "price": 1200.5, "is_offer": True, "description": "A gaming laptop"}
```
Response will be

```json
    {
        "name": "Laptop",
        "price": 1200.5,
        "is_offer": true
    }
```