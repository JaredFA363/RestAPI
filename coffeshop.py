from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    item_name: str
    price: float
    is_available: bool = True

# non-persistent storage
menu_items = []

@app.get("/")
def read_root():
    return {"Welcome": "to the Coffee Shop API"}

@app.post("/menu-items")
def create_menu_item(item:Item):
    menu_items.append(item)
    return menu_items

@app.get("/menu")
def list_menu_items(limit: int = 10):
    return menu_items[0:limit]

@app.get("/menu/{item_id}")
def get_menu_item(item_id: int) -> Item:
    if item_id < len(menu_items):
        return menu_items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Menu item {item_id} not found")
    
@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    if item_id < len(menu_items):
        deleted_item = menu_items.pop(item_id)
        return {"detail": f"Menu item {item_id} deleted", "item":deleted_item}
    
@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, item: Item):
    if item_id < len(menu_items):
        menu_items[item_id] = item
        return menu_items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Menu item {item_id} not found")