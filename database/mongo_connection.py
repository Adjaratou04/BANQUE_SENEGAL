from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "Baqnues_senegal")

    if not uri:
        raise ValueError("MONGO_URI n'est pas définie")

    client = MongoClient(uri)
    db = client[db_name]
    return db
