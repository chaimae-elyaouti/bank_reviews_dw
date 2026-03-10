import os
import json
import logging
from dotenv import load_dotenv
from apify_client import ApifyClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_TOKEN:
    raise ValueError("Clé API introuvable. Vérifiez votre fichier .env")

client = ApifyClient(APIFY_TOKEN)

def extract_bank_reviews_massively(banques, villes, max_agences=5, max_avis=150):
    """
    Scrape Google Maps pour plusieurs banques sur plusieurs villes.
    Renvoie une liste contenant toutes les données brutes.
    """
    toutes_les_donnees = []
    for ville in villes:
        for banque in banques:
            recherche = f"{banque} {ville}"
            logging.info(f"Lancement du robot distant pour : '{recherche}'...")
            
            run_input = {
                "searchStringsArray": [recherche],
                "language": "fr",
                "maxCrawledPlacesPerSearch": max_agences,
                "maxReviews": max_avis,
                "reviewsSort": "newest",
            }

            try:
                run = client.actor("compass/crawler-google-places").call(run_input=run_input)
                donnees_locales = client.dataset(run["defaultDatasetId"]).list_items().items
                toutes_les_donnees.extend(donnees_locales)
                logging.info(f"Succès pour '{recherche}'. {len(donnees_locales)} agences extraites.")
            
            except Exception as e:
                logging.error(f"Échec de l'extraction pour '{recherche}': {e}")
                
    return toutes_les_donnees

if __name__ == "__main__":
        
    banques_cibles = ["CIH Bank", "Attijariwafa Bank", "Banque Populaire", "Umnia Bank"]
    villes_cibles = ["Casablanca", "Rabat"]
    
    logging.info("Démarrage de la grande collecte de données (Cela va prendre 10 à 15 minutes)...")
    
    donnees_brutes = extract_bank_reviews_massively(
        banques=banques_cibles, 
        villes=villes_cibles, 
        max_agences=5, 
        max_avis=150
    )
    
    dossier_raw = "data/raw"
    os.makedirs(dossier_raw, exist_ok=True)
    chemin_fichier = os.path.join(dossier_raw, "maroc_banks_reviews_raw.json")
    
    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(donnees_brutes, fichier, ensure_ascii=False, indent=4)
        
    logging.info(f"SUCCÈS TOTAL : Données sauvegardées dans '{chemin_fichier}'.")