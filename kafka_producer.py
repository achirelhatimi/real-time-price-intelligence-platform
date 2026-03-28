from kafka import KafkaProducer
import json

# Connexion à Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode('utf-8')
)

def envoyer_produit(produit):
    producer.send('prix-jumia', value=produit)
    print(f"Envoyé : {produit['nom']} - {produit['prix']}")

# Test — envoyer un produit fictif
produit_test = {
    "nom": "iPhone 17 Pro Max",
    "marque": "Apple",
    "prix": 16375.0,
    "ancien_prix": 22999.0,
    "remise": 29.0,
    "date_scraping": "2026-03-06 22:00:00"
}

envoyer_produit(produit_test)
producer.flush()
print("Message envoyé dans Kafka avec succès !")