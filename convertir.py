import json

with open(r"C:\jumia_scraper\produits_propres.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open(r"C:\jumia_scraper\produits_bigquery.jsonl", "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Conversion terminée : {len(data)} lignes")
