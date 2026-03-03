import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_TOKEN:
    raise ValueError("Clé API introuvable !")

client = ApifyClient(APIFY_TOKEN)



def extraire_donnees_google_maps(recherche, max_agences=3, max_avis=50):
    """
    Envoie une requête aux serveurs d'Apify pour scraper Google Maps.
    """
    print(f"[INFO] Lancement du robot distant pour : '{recherche}'...")
    run_input = {
        "searchStringsArray": [recherche],
        "language": "fr",
        "maxCrawledPlacesPerSearch": max_agences,
        "maxReviews": max_avis, 
        "reviewsSort": "newest", # pour forcer l'Actor Apify à scraper le bloc des avis, sinon il ne renvoie que les métadonnées de l'agence.
    }

    print("[INFO] Extraction en cours sur le Cloud Apify...")
    run = client.actor("compass/crawler-google-places").call(run_input=run_input)

    print("Extraction terminée ! Téléchargement des données en cours...")
    donnees = client.dataset(run["defaultDatasetId"]).list_items().items

    return donnees



if __name__ == "__main__":

    donnees_brutes = extraire_donnees_google_maps("CIH Bank Rabat", max_agences=2, max_avis=50)
    
    dossier_raw = "data/raw"    
    chemin_fichier = os.path.join(dossier_raw, "cih_rabat_raw.json")
    
    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(donnees_brutes, fichier, ensure_ascii=False, indent=4)
        
    print(f"SUCCÈS TOTAL : Les données de {len(donnees_brutes)} agences ont été sauvegardées dans '{chemin_fichier}' !")