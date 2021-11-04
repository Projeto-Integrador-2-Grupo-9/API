from .db import database

collection = database["Floater"]


class Floater:

    def __init__(self, mac_address, starting_position) -> None:
        self.mac_address = mac_address
        self.starting_position = starting_position

    def create(self):

        query = {"mac_address": self.mac_address,
                 "starting_position": self.starting_position}
        result = collection.count_documents(query)

        if result > 0:
            print(
                f"[!] started existing floater {self.mac_address}", flush=True)
            return collection.find(query)

        print(
            f"[!] created and started floater {self.mac_address}", flush=True)
        return collection.insert_one(query)
