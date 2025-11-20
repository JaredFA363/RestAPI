## Building a REST API with FastAPI
## https://medium.com/@ramjoshi.blogs/building-rest-apis-with-python-and-fastapi-f0e9ae19905c

# Principles of REST:
# Resource identification through URI
# Uniform interface for interacting with resources
# Self-descriptive messages
# Hypermedia as the engine of application state (HATEOAS)

# Basic config
from asyncio import tasks
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import databases
database = databases.Database("sqlite:///./test.db")

app = FastAPI()
items = []

# Endpoints
# They are the primary way that clients interact with REST API
# is a URL that clients can send requests to and the sercr will respond accordingly
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


#Uses Pydantics - a data validation library
# to define the structure of the data being sent and received
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# POSTING (CREATING) Items
@app.post("/items/")
async def create_item(item: Item):
    return item

# Get 1 singular item
@app.get("/items/{item_id}")
def read_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# POSTING (CREATING) Items
@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    item_dict["id"] = len(items) + 1
    items.append(item_dict)
    return item_dict

# route for updating an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    for i, existing_item in enumerate(items):
        if existing_item["id"] == item_id:
            items[i] = item.dict()
            items[i]["id"] = item_id
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")

# route for deleting an existing item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(i)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

class Task(BaseModel):
    title: str
    description: str

@app.post("/tasks")
async def create_task(task: Task):
    query = tasks.insert(). values(
        title=task.title,
        description=task.description,
        completed=False
    )
    task_id = await database.execute(query)
    return {"id": task_id, **task.dict(), "completed": False}