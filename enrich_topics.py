import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import nltk
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaModel
import re


nltk.download('stopwords')
nltk.download('punkt')

def get_connection():
    basedir = Path(__file__).resolve().parent
    env_path = basedir / '.env'
    
    # Charge le fichier en utilisant le chemin complet
    load_dotenv(dotenv_path=env_path)
    
    # Debug pour toi : voir si le script trouve le fichier
    # print(f"DEBUG: Recherche du .env ici : {env_path}")
    # print(f"DEBUG: Fichier trouvé ? {env_path.exists()}")

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")

    if not all([dbname, user, password, host]):
        raise ValueError(f"Variables vides. Chemin testé : {env_path}")

    return psycopg2.connect(
        host=host, 
        database=dbname, 
        user=user, 
        password=password, 
        port="5432"
    )

def preprocess_text(text):
    # Nettoyage simple : minuscules, suppression ponctuation et chiffres
    text = re.sub(r'\d+', '', text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    
    # Stopwords (Français + quelques mots bancaires inutiles)
    stop_words = set(stopwords.words('french'))
    stop_words.update(['banque', 'cih', 'attijari', 'plus', 'tout', 'faire'])
    
    return [t for t in tokens if t not in stop_words and len(t) > 3]

def enrich_topics():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # 1. Récupération des avis (On se concentre sur le Français pour le LDA)
    cur.execute("SELECT review_id, review_text FROM stg_enriched_reviews WHERE language = 'fr'")
    rows = cur.fetchall()
    
    if not rows:
        print("Aucun avis à traiter.")
        return

    # 2. Préparation des données pour Gensim
    documents = [preprocess_text(r['review_text']) for r in rows]
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]

    # 3. Entraînement du modèle LDA (On cherche 5 thèmes)
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10)

    # 4. Ajout de la colonne topic si elle n'existe pas
    cur.execute("ALTER TABLE stg_enriched_reviews ADD COLUMN IF NOT EXISTS topic_id INTEGER;")
    cur.execute("ALTER TABLE stg_enriched_reviews ADD COLUMN IF NOT EXISTS topic_label TEXT;")

    # 5. Assignation du topic dominant à chaque avis
    print("Assignation des thèmes en cours...")
    for i, row in enumerate(rows):
        bow = corpus[i]
        topics = lda_model.get_document_topics(bow)
        # On prend le topic avec le score le plus élevé
        dominant_topic = max(topics, key=lambda x: x[1])[0]
        
        cur.execute(
            "UPDATE stg_enriched_reviews SET topic_id = %s WHERE review_id = %s",
            (int(dominant_topic), row['review_id'])
        )

    conn.commit()
    print("Succès ! Les thèmes ont été extraits et enregistrés.")
    
    # Affichage des thèmes trouvés pour ton analyse
    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic {idx}: {topic}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    enrich_topics()