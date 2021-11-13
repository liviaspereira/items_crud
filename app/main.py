from typing import Optional

from fastapi import FastAPI, status

from pydantic import BaseModel



class Item(BaseModel):
    name: str
    description: Optional[str] = "Padrão"
    price: float
    tax: Optional[float] = None
    id: Optional[int] = None


app = FastAPI()
lista = []


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item.id = len(lista)
    lista.append(item)
    return item

@app.put("/items/{item_id}", status_code=status.HTTP_201_CREATED)
def update_item(item: Item, item_id: int):
    item.id = item_id
    lista[item_id] = item
    return item
    
@app.get("/items/")
def list_items():
    return lista




