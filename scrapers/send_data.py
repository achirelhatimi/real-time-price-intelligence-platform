import requests
import json
from datetime import datetime

data = {
    "product_id": "A1",
    "price": 249.99,
    "timestamp": datetime.now().isoformat()
}

response = requests.post(
    "http://localhost:8080/contentListener",  # ← path ajouté
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

print(response.status_code)  # doit retourner 200