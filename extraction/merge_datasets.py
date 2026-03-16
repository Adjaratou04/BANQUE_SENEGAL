import pandas as pd

# Charger la base existante
base = pd.read_excel("data/BASE_SENEGAL2.xlsx")

# Charger les nouvelles données (2021-2022)
new_data = pd.read_excel("data/extracted_tables/banques_senegal_2021_2022.xlsx")

# Vérifier les colonnes
print("Colonnes base :", base.columns)
print("Colonnes nouvelles :", new_data.columns)

# Fusionner les datasets
dataset_final = pd.concat([base, new_data], ignore_index=True)

# Sauvegarder
dataset_final.to_excel("data/extracted_tables/dataset_banques_senegal_complet.xlsx", index=False)

print("Dataset fusionné créé avec succès")