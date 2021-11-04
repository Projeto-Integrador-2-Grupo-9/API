from pymongo import MongoClient


mongo_client = MongoClient("mongodb://root:example@mongo:27017/")

database = mongo_client["AquaData_API"]
