import os
import json
import logging
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def connect_to_db():
    """Crée et retourne une connexion à PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME")
        )
        return conn
    except Exception as e:
        logging.error(f"Erreur de connexion à la base de données : {e}")
        return None

def create_staging_table(conn):
    """Crée la table brute avec une Clé Primaire stricte pour éviter les doublons."""
    with conn.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS staging_bank_reviews (
            review_id VARCHAR(255) PRIMARY KEY,  -- L'ID unique fourni par Google/Apify
            bank_name VARCHAR(255),
            branch_address TEXT,
            reviewer_name VARCHAR(255),
            stars INTEGER,
            review_text TEXT,
            published_date VARCHAR(100),
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
    conn.commit()
    logging.info("Table 'staging_bank_reviews' prête.")

def load_json_to_postgres(filepath, conn):
    """Prépare les données et réalise un Bulk Insert (Insertion en masse)."""
    if not os.path.exists(filepath):
        logging.warning(f"Le fichier {filepath} n'existe pas.")
        return

    with open(filepath, 'r', encoding='utf-8') as file:
        agences = json.load(file)

    data_to_insert = []
    
    for agence in agences:
        bank_name = agence.get("title", "Inconnu")
        branch_address = agence.get("address", "Adresse inconnue")
        
        for avis in agence.get("reviews", []):
            review_id = avis.get("reviewId")
            if not review_id:
                continue 
                
            reviewer_name = avis.get("name", "Anonyme")
            stars = avis.get("stars", 0)
            review_text = avis.get("text", "Pas de texte")
            published_date = avis.get("publishedAtDate", "Date inconnue")
            data_to_insert.append((review_id, bank_name, branch_address, reviewer_name, stars, review_text, published_date))

    insert_query = """
        INSERT INTO staging_bank_reviews 
        (review_id, bank_name, branch_address, reviewer_name, stars, review_text, published_date)
        VALUES %s
        ON CONFLICT (review_id) DO NOTHING; -- Idempotence : On ignore les doublons !
    """

    with conn.cursor() as cursor:
        execute_values(cursor, insert_query, data_to_insert)
        
    conn.commit()
    logging.info(f"{len(data_to_insert)} avis traités. Les nouveaux ont été ajoutés, les doublons ignorés.")


if __name__ == "__main__":
    fichier_json = "data/raw/maroc_banks_reviews_raw.json"    
    logging.info("Tentative de connexion à PostgreSQL...")
    connexion = connect_to_db()
    
    if connexion:
        create_staging_table(connexion)
        logging.info(f"Début de l'injection en masse depuis {fichier_json}...")
        load_json_to_postgres(fichier_json, connexion)
        
        connexion.close()
        logging.info("Connexion fermée proprement.")