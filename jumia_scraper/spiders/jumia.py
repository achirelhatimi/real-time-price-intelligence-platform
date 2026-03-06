import scrapy
from bs4 import BeautifulSoup
import json
from datetime import datetime
from kafka import KafkaProducer

class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.ma"]
    
    start_urls = [
        "https://www.jumia.ma/telephone-tablette/",
        "https://www.jumia.ma/electronique/",
        "https://www.jumia.ma/ordinateurs-accessoires-informatique/",
    ]

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode('utf-8')
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        script = soup.find("script", string=lambda t: t and "window.__STORE__" in t)
        
        if not script:
            return
        
        data = json.loads(script.text.split("window.__STORE__=")[1].rstrip(";"))
        produits = data.get("products", [])
        
        for produit in produits:
            item = {
                "nom": produit.get("displayName", ""),
                "marque": produit.get("brand", ""),
                "prix": produit["prices"].get("price", ""),
                "ancien_prix": produit["prices"].get("oldPrice", ""),
                "remise": produit["prices"].get("discount", ""),
                "rating": produit.get("rating", {}).get("average", 0),
                "url": "https://www.jumia.ma" + produit.get("url", ""),
                "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Envoyer directement dans Kafka
            self.producer.send('prix-jumia', value=item)
            print(f"Kafka ← {item['nom']} - {item['prix']}")
            
            yield item
        
        page_actuelle = response.meta.get("page", 1)
        prochaine_page = page_actuelle + 1
        prochaine_url = f"{response.url.split('?')[0]}?page={prochaine_page}"
        
        if produits:
            yield scrapy.Request(
                url=prochaine_url,
                callback=self.parse,
                meta={"page": prochaine_page}
            )
    
    def closed(self, reason):
        self.producer.flush()
        self.producer.close()