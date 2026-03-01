import logging
from playwright.sync_api import sync_playwright
import time

# Configuration du journal (Logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GoogleMapsScraper:
    def __init__(self):
        logging.info("Démarrage du moteur Playwright...")
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(locale="fr-FR") 
        self.page = self.context.new_page()
        self.base_url = "https://www.google.com/maps"

    def fermer(self):
        self.browser.close()
        self.playwright.stop()
        logging.info("Navigateur fermé proprement.")

    def ouvrir_et_gerer_cookies(self):
        logging.info(f"Navigation vers {self.base_url}...")
        self.page.goto(self.base_url)

        try:
            logging.info("Recherche du bouton de cookies...")
            bouton_cookies = self.page.locator("button:has-text('Tout refuser')")
            bouton_cookies.wait_for(timeout=5000) 
            bouton_cookies.click()
            logging.info("Popup des cookies refusée avec succès.")
        except Exception as e:
            logging.info("Aucun popup de cookies détecté, on continue.")

    def chercher_agence(self, nom_banque, ville):
        query = f"{nom_banque} {ville}"
        logging.info(f"Recherche de l'agence : {query}")
        
        try:
            barre_recherche = self.page.locator('input[name="q"]')
            barre_recherche.wait_for(timeout=5000)
            barre_recherche.fill(query)
            self.page.keyboard.press("Enter")
            
            logging.info("Attente de la liste des agences...")
            self.page.wait_for_selector('a.hfpxzc', timeout=10000)
            
            liste_agences = self.page.locator('a.hfpxzc')
            
            logging.info("Clic sur la première agence trouvée...")
            liste_agences.first.click()
            
            self.page.wait_for_timeout(5000)
            logging.info("Fiche de l'agence ouverte !")
            
        except Exception as e:
            logging.error(f"Erreur lors de la recherche : {e}")

    def ouvrir_onglet_avis(self):
        logging.info("Recherche de l'onglet 'Avis'...")
        
        try:
            onglet_avis = self.page.locator("button:has-text('Avis'), button:has-text('Reviews')").first
            onglet_avis.wait_for(timeout=5000)
            
            onglet_avis.click()
            logging.info("Onglet 'Avis' ouvert avec succès !")
            
            self.page.wait_for_timeout(3000)
            
        except Exception as e:
            logging.error(f"Impossible de trouver l'onglet Avis : {e}")

if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    
    scraper.ouvrir_et_gerer_cookies()
    
    scraper.chercher_agence("CIH Bank", "Rabat")

    scraper.ouvrir_onglet_avis()
    
    time.sleep(5) 
    
    scraper.fermer()