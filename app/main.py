from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .clients.mqtt import MQTT_Client
import requests
from app.clients import mqtt

from .db import database

collection = database["Floater"]


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt_client = MQTT_Client()
mqtt_client.start()


@app.get("/")
def read_root():

    return {"Connection": "successful"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/floaters_position")
def get_floaters_position():

    floaters_position = []

    floaters = collection.find({})

    counter = 1

    for floater in floaters:

        data = dict({
            "mac_address": floater["mac_address"]
        })

        position = requests.get(
            'http://ad_ate/last_log',
            json=data,
            headers={
                "Content-Type": "application/json; charset=utf-8"
            }
        )

        floaters_position.append({
            "mac_address": floater["mac_address"],
            "position": position.json(),
            "id": counter
        })

        counter = counter + 1

    return floaters_position


class Device(BaseModel):
    mac_address: str


@app.post("/last_log")
def get_sensor_data(device: Device):

    response = requests.get(
        'http://ad_pos/last_log',
        json=dict(device),
        headers={
            "Content-Type": "application/json; charset=utf-8"
        }
    )

    return response.json()
