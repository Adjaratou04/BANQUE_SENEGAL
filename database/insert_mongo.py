import pandas as pd
from mongo_connection import get_database

# charger dataset final
df = pd.read_excel("data/extracted_tables/dataset_banques_senegal_clean.xlsx")

# connexion DB
db = get_database()

collection = db["banques"]

# convertir dataframe
records = df.to_dict("records")

# insertion
collection.insert_many(records)

print("Données insérées dans MongoDB")