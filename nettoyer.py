print("le code tourne")

import pandas as pd

df = pd.read_json("produits.json")

print(f"Avant nettoyage : {len(df)} produits")

# Nettoyer le prix
df["prix"] = pd.to_numeric(
    df["prix"].str.replace(" Dhs", "").str.replace(",", "").str.split(" - ").str[0],
    errors="coerce"
)

# Nettoyer l'ancien prix
df["ancien_prix"] = pd.to_numeric(
    df["ancien_prix"].str.replace(" Dhs", "").str.replace(",", "").str.split(" - ").str[0],
    errors="coerce"
)

# Nettoyer la remise
df["remise"] = pd.to_numeric(
    df["remise"].str.replace("%", ""),
    errors="coerce"
)

# Supprimer les doublons
df.drop_duplicates(subset=["url"], inplace=True)

print(f"Après nettoyage : {len(df)} produits")
print(df.head())

# Sauvegarder
df.to_json("produits_propres.json", orient="records", force_ascii=False)
print("Fichier sauvegardé : produits_propres.json")