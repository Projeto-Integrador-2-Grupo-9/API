from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


@app.get("/")
def read_root():
    client = MongoClient()

    return {"Connection": "successful"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
