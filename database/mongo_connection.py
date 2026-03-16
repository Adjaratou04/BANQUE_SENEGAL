from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    # Nom exact de la base de données dans MongoDB Atlas
    client = MongoClient(uri)
    db = client["Baqnues_senegal"]
    return db