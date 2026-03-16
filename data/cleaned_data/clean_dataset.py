import pandas as pd

# Charger le dataset fusionné
df = pd.read_excel("data/extracted_tables/dataset_banques_senegal_complet.xlsx")

# 1️⃣ supprimer les doublons
df = df.drop_duplicates()

# 2️⃣ corriger les sigles (uniformiser)
df["Sigle"] = df["Sigle"].str.upper()

# 3️⃣ remplacer les valeurs vides par 0 pour les colonnes numériques
numeric_cols = df.select_dtypes(include=["float64","int64"]).columns
df[numeric_cols] = df[numeric_cols].fillna(0)

# 4️⃣ convertir ANNEE en entier
df["ANNEE"] = df["ANNEE"].astype(int)

# 5️⃣ supprimer lignes sans banque
df = df[df["Sigle"].notna()]

# Sauvegarder
df.to_excel("data/extracted_tables/dataset_banques_senegal_clean.xlsx", index=False)

print("Dataset nettoyé créé")