from typing import Optional

from fastapi import FastAPI, status, HTTPException

from pydantic import BaseModel

from sqlmodel import Field, SQLModel, create_engine, Session, select


class Item(SQLModel, table=True):
    name: str
    description: Optional[str] = "Padrão"
    price: float
    tax: Optional[float] = None
    id: Optional[int] = Field(default=None, primary_key=True)

postgres_url = "postgresql://postgres:123@localhost:5432/postgres"
engine = create_engine(postgres_url, echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/items/")
def list_items():
    with Session(engine) as session:
        statement = select(Item)
        results = session.exec(select(Item)).all()
    return results


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)   
        session.commit()
        session.refresh(item)
    return item


@app.put("/items/{item_id}", status_code=status.HTTP_201_CREATED)
def update_item(name: str, item_id: int):
    with Session(engine) as session:
        item = session.exec(select(Item.where(Item.id == item_id))).one()
        item.name = name
        session.add(item)
        session.commit()
        session.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    with Session(engine) as session:
        try:
            item = session.exec(select(Item).where(Item.id == item_id)).one()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        session.delete(item)
        session.commit()