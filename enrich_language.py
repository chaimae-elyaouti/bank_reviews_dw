import psycopg2
import re
from langdetect import detect, DetectorFactory
from psycopg2.extras import RealDictCursor
from db_utils import get_connection

DetectorFactory.seed = 0
def clean_language(detected_lang, text):
    text_lower = text.lower()
    
    is_darija_pattern = re.search(r'[a-zA-Z][379]|[379][a-zA-Z]', text_lower)
    
    if is_darija_pattern:
        return 'darija_latin'

    if detected_lang in ['fr', 'ar', 'en']:
        return detected_lang

    fr_keywords = {'service', 'agence', 'banque', 'client', 'nul', 'zero', 'merci', 'bonjour', 'accueil'}
    words_in_text = set(text_lower.split())
    if not words_in_text.isdisjoint(fr_keywords):
        return 'fr'
    
    return 'fr'

def enrich_data():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("ALTER TABLE stg_enriched_reviews ADD COLUMN IF NOT EXISTS language VARCHAR(25);")
    cur.execute("ALTER TABLE stg_enriched_reviews ALTER COLUMN language TYPE VARCHAR(25);")
    cur.execute("SELECT review_id, review_text FROM stg_enriched_reviews")
    rows = cur.fetchall()
    
    print(f"Mise à jour de {len(rows)} avis...")

    for row in rows:
        text = row['review_text']
        rid = row['review_id']
        
        try:
            detected = detect(text)
            lang = clean_language(detected, text)
        except:
            lang = "unknown"
            
        cur.execute(
            "UPDATE stg_enriched_reviews SET language = %s WHERE review_id = %s",
            (lang, rid)
        )

    conn.commit()
    print("Succès ! Toutes les langues ont été enregistrées dans PostgreSQL.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    enrich_data()