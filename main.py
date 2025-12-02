from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


inventory = {
        1: {"item_id": 2,
        "name": "steak",
        "price": 12.89
        }
    }

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="Id of item you want to view"), gt = 1):
    return inventory[item_id]

@app.get("/get-by-name/")
def get_item(*, name: Optional[str] = None, item_id: Optional[int] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name or inventory[item_id]["item_id"] == item_id:
            return inventory[item_id]
        
    return {"Data": "Not found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error" : "Item ID already exists"}

    # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price} 
    new_item = Item()
    return inventory[item_id]


# @app.get("/")
# def home():
#     return {"Data": "Black Friday!!!"}

# @app.get("/about")
# def about():
#     return{"Data": "About"}