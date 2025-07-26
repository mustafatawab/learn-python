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



Run the Server
``` uvicorn main:app --reload |  fastapi dev main.py   ```
