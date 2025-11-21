from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str = None # remove default value to make it required e.g. text: str
    is_done: bool = False


# none persistent storage
items = []

# first get method
# to run use uvicorn main:app --reload
# or try this: python -m uvicorn main:app --reload
@app.get("/")
def read_root():
    return {"Hello": "World"}

# creating an item -> POST request to the items path
@app.post("/items")
def create_item(item: Item):# change from str: # This currently is a query string in a path but this isnt the right way to do it so instaed we should use a JSON payload.
    items.append(item)
    return items

# get the first x items
@app.get("/items") # this will hit the /items path mainly because of the different request type. GET
def list_items(limit: int = 10):
    return items[0:limit]

## to use payload we need a pydantics model
## so instead of this: curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple' like normal
## we use this: curl -X POST -H "Content-Type: application/json" -d '{"text":"apple","is_done":false}' 'http://127.0.0.1:8000/items'

#get singular item by id
@app.get("/items/{item_id}") # can add a response model here to validate the output for clientside so they know what to expect e.g. response_model=Item
def get_items(item_id: int) -> Item: # change from -> str means we have to use a json payload instead of just use in the path
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
# can use fastapi's automatic docs at /docs or /redoc to test the api as well
# 127.0.0.1:8000/docs

# FASTAPI IS ASYNC BY DEFAULT
# so we can make our functions async if needed
# also is easy to use
# but does have less adoption than flask or django and support for some libraries may be limited