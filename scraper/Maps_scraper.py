import logging
from playwright.sync_api import sync_playwright
import time
import csv

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
            premiere_agence = liste_agences.first
            nom_agence = premiere_agence.get_attribute("aria-label")
            logging.info(f"L'AGENCE CIBLÉE EST : {nom_agence}")
            premiere_agence.click()
            self.page.wait_for_selector('h1', timeout=5000)
            self.page.wait_for_timeout(2000) # Petite pause humaine
            logging.info("Fiche de l'agence ouverte et prête !")
            
        except Exception as e:
            logging.error(f"Erreur lors de la recherche : {e}")

    def ouvrir_onglet_avis(self):
        logging.info("Recherche de l'onglet 'Avis'...")
        
        try:
            selecteur_onglet = 'button[role="tab"]:has-text("Avis"), button[role="tab"]:has-text("Reviews")'
            
            onglet_avis = self.page.locator(selecteur_onglet).first
            
            onglet_avis.wait_for(timeout=5000)
            
            onglet_avis.click()
            logging.info("✅ Onglet 'Avis' cliqué avec succès !")
            
            self.page.wait_for_timeout(3000)
            
        except Exception as e:
            logging.error(f"Impossible de trouver l'onglet Avis : {e}")


    def scroller_avis(self, objectif_avis=20):
        """Scrolle la liste des avis jusqu'à atteindre le nombre ciblé."""
        logging.info(f"Début du scroll pour atteindre au moins {objectif_avis} avis...")
        selecteur = ".jftiEf" # On garde ce sélecteur, c'est le bon parent global !
        
        # 🌟 L'ASTUCE DU PRO : LE COUP DE MOLETTE 🌟
        # On donne un coup de molette vers le bas pour dépasser les filtres
        # et forcer Google à "réveiller" ses commentaires.
        logging.info("Petit coup de molette pour passer les filtres...")
        self.page.mouse.wheel(delta_x=0, delta_y=800) 
        self.page.keyboard.press("PageDown") # Et un coup de touche Page Suivante par sécurité
        self.page.wait_for_timeout(2000) # On laisse 2 secondes à Google pour réagir
        
        try:
            logging.info("Attente de l'apparition du premier avis (max 10s)...")
            self.page.wait_for_selector(selecteur, timeout=10000)
        except Exception:
            logging.error("❌ Aucun avis trouvé malgré le coup de molette.")
            self.page.screenshot(path="erreur_robot.png")
            return 
            
        try:
            while True:
                compte_actuel = self.page.locator(selecteur).count()
                logging.info(f"Avis actuellement chargés : {compte_actuel}")
                
                if compte_actuel >= objectif_avis:
                    logging.info("🎯 Objectif atteint ! On arrête le scroll.")
                    break
                
                dernier_avis = self.page.locator(selecteur).nth(compte_actuel - 1)
                dernier_avis.scroll_into_view_if_needed()
                
                self.page.wait_for_timeout(3000)
                
                nouveau_compte = self.page.locator(selecteur).count()
                if nouveau_compte == compte_actuel:
                    logging.info("Fin de la liste atteinte ou chargement bloqué. On arrête.")
                    break
                    
        except Exception as e:
            logging.error(f"Erreur pendant le scroll : {e}")
    

    def extraire_avis(self):
        """Extrait les données (Nom, Note, Date, Texte) des avis chargés."""
        logging.info("Début de l'extraction des données...")
        avis_extraits = []
        
        try:
            boites_avis = self.page.locator(".jftiEf").all()
            logging.info(f"{len(boites_avis)} avis trouvés à extraire.")
            
            for boite in boites_avis:
                # 1. Le nom
                try:
                    nom = boite.locator('.d4r55').inner_text()
                except:
                    nom = "Inconnu"
                    
                # 2. La note
                try:
                    note = boite.locator('span[role="img"]').get_attribute("aria-label")
                except:
                    note = "Non noté"
                    
                # 3. La date
                try:
                    date_avis = boite.locator('.rsqaWe').inner_text()
                except:
                    date_avis = "Date inconnue"
                    
                # 4. Le texte (LA CORRECTION EST ICI 🌟)
                try:
                    # On ajoute .first pour éviter l'erreur si Google a traduit le texte !
                    texte = boite.locator('.wiI7pd').first.inner_text()
                    
                    if texte:
                        texte = texte.strip()
                        
                    if not texte:
                        texte = "Juste une note (Aucun commentaire)"
                except:
                    texte = "Juste une note (Aucun commentaire)"
                    
                avis_extraits.append({
                    "nom": nom,
                    "note": note,
                    "date": date_avis,
                    "texte": texte
                })
            
            logging.info("✅ Extraction terminée !")
            
            print("\n" + "="*40)
            print("📊 APERÇU DES DONNÉES EXTRAITES 📊")
            print("="*40)
            for i, avis in enumerate(avis_extraits[:5]): # On affiche les 5 premiers pour mieux voir
                print(f"Avis n°{i+1}")
                print(f"👤 Nom   : {avis['nom']}")
                print(f"⭐ Note  : {avis['note']}")
                print(f"📅 Date  : {avis['date']}")
                print(f"📝 Texte : {avis['texte']}")
                print("-" * 40)
                
            return avis_extraits
                
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction : {e}")
            return []
        
    
    def sauvegarder_csv(self, donnees, nom_fichier="avis_banque.csv"):
        """Sauvegarde la liste des dictionnaires dans un fichier CSV."""
        if not donnees:
            logging.warning("⚠️ Aucune donnée à sauvegarder.")
            return

        logging.info(f"Préparation de la sauvegarde dans {nom_fichier}...")
        
        try:
            # Les noms des colonnes (les clés de notre dictionnaire)
            colonnes = ["nom", "note", "date", "texte"]
            
            # On ouvre un nouveau fichier en mode écriture ('w') avec l'encodage utf-8 (pour les accents et l'arabe)
            with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier:
                writer = csv.DictWriter(fichier, fieldnames=colonnes)
                
                # On écrit la première ligne (les en-têtes)
                writer.writeheader()
                
                # On écrit toutes les données d'un coup !
                writer.writerows(donnees)
                
            logging.info(f"💾 SUCCÈS : {len(donnees)} avis sauvegardés dans le fichier '{nom_fichier}' !")
            
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde CSV : {e}")

if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    
    scraper.ouvrir_et_gerer_cookies()
    scraper.chercher_agence("CIH Bank", "Rabat")
    scraper.ouvrir_onglet_avis()
    scraper.scroller_avis(objectif_avis=20)
    
    # On récupère les données dans une variable
    donnees_extraites = scraper.extraire_avis()
    
    # 🌟 NOUVELLE ACTION : On sauvegarde les données dans un vrai fichier !
    scraper.sauvegarder_csv(donnees_extraites, "cih_rabat_reviews.csv")
    
    time.sleep(2) 
    scraper.fermer()