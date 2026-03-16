from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    # Affiche toutes les bases disponibles dans les logs Render
    try:
        print("BASES DISPONIBLES:", client.list_database_names())
    except Exception as e:
        print("ERREUR CONNEXION:", e)
    db = client["Baqnues_senegal"]
    print("COLLECTIONS:", db.list_collection_names())
    return db