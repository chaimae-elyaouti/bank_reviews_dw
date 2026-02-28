import logging
from playwright.sync_api import sync_playwright
import time

# 1. Configuration du journal (Logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GoogleMapsScraper:
    def __init__(self):
        """Initialise le robot et ouvre le navigateur."""
        logging.info("Démarrage du moteur Playwright...")
        self.playwright = sync_playwright().start()
        
        # HEADLESS=False : Très important au début ! 
        # Ça permet de voir le navigateur s'ouvrir. 
        # En production (Phase 5), on le mettra sur True pour qu'il soit invisible.
        self.browser = self.playwright.chromium.launch(headless=False)
        
        # On force la langue en français pour être sûr du nom des boutons
        self.context = self.browser.new_context(locale="fr-FR") 
        self.page = self.context.new_page()
        
        self.base_url = "https://www.google.com/maps"

    def fermer(self):
        """Ferme proprement le navigateur à la fin."""
        self.browser.close()
        self.playwright.stop()
        logging.info("Navigateur fermé proprement.")

    def ouvrir_et_gerer_cookies(self):
        """Va sur Google Maps et essaie de fermer la fenêtre des cookies."""
        logging.info(f"Navigation vers {self.base_url}...")
        self.page.goto(self.base_url)

        # Gestion des cookies (Le bloc Try/Except professionnel)
        try:
            logging.info("Recherche du bouton de cookies...")
            # On cherche un bouton qui contient le texte "Tout refuser"
            bouton_cookies = self.page.locator("button:has-text('Tout refuser')")
            
            # On attend maximum 5 secondes (5000 millisecondes)
            bouton_cookies.wait_for(timeout=5000) 
            
            # S'il le trouve, il clique !
            bouton_cookies.click()
            logging.info("✅ Popup des cookies refusée avec succès.")
            
        except Exception as e:
            # Si le bouton n'apparaît pas au bout de 5 secondes, ça vient ici.
            logging.info("ℹ️ Aucun popup de cookies détecté, on continue.")

# --- POINT D'ENTRÉE DU SCRIPT ---
if __name__ == "__main__":
    # On crée notre robot
    scraper = GoogleMapsScraper()
    
    # On lance l'action
    scraper.ouvrir_et_gerer_cookies()
    
    # On fait une pause de 5 secondes juste pour que tu aies le temps 
    # d'admirer le résultat sur ton écran !
    time.sleep(5) 
    
    # On nettoie tout
    scraper.fermer()