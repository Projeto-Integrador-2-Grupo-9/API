import paho.mqtt.client as mqtt
from ..floater import Floater
import json
import requests

MQTT_CLIENT_NAME = "AquaData_MAIN_API"
BROKER_URL = "test.mosquitto.org"


def on_message(client, userdata, message):

    payload = message.payload.decode("utf-8")
    topic = message.topic

    if topic == "AD/devices":
        mac_address = json.loads(payload)["new_device"]
        starting_position = json.loads(payload)["starting_position"]
        floater = Floater(mac_address=mac_address,
                          starting_position=starting_position)
        floater.create()

        print(f"[!] message recieved at [{topic}] {payload}", flush=True)

    if topic == "AD/sensor_data":
        print(f"[*] message recieved at [{topic}] {payload}", flush=True)
        requests.post('http://ad_pos/log', data=payload)

    if topic == "AD/position_data":
        print(f"[#] message recieved at [{topic}] {payload}", flush=True)
        requests.post('http://ad_ate/log', data=payload)


class MQTT_Client():

    def __init__(self):

        self.client = mqtt.Client(MQTT_CLIENT_NAME)
        self.client.on_message = on_message

    def start(self):
        self.client.connect(BROKER_URL)
        self.client.loop_start()
        self.client.subscribe("AD/devices")
        self.client.subscribe("AD/sensor_data")
        self.client.subscribe("AD/position_data")
