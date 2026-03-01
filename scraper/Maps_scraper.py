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
            logging.info("Texte tapé avec succès.")
            
            self.page.keyboard.press("Enter")
            
            self.page.wait_for_timeout(5000)
            logging.info(" Recherche validée !")
            
        except Exception as e:
            logging.error(f"Erreur lors de la recherche : {e}")


if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    
    scraper.ouvrir_et_gerer_cookies()
    
    scraper.chercher_agence("CIH Bank", "Rabat")
    
    time.sleep(5) 
    
    scraper.fermer()