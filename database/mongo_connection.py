from pymongo import MongoClient

def get_database():

    client = MongoClient("mongodb://localhost:27017")

    db = client["banques_senegal"]

    return db