from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_CONNECTION_STRING)
mongo_db = mongo_client["practice"]
mongo_collection = mongo_db["users"]
