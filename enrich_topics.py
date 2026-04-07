import psycopg2
from psycopg2.extras import RealDictCursor
import nltk
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaModel
import re
from db_utils import get_connection

# Configuration NLTK
nltk.download(['stopwords', 'punkt', 'punkt_tab'], quiet=True)

def preprocess_text(text):
    """Nettoyage des avis : suppression ponctuation, chiffres et stop-words métiers."""
    text = re.sub(r'\d+', '', text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    
    stop_words = set(stopwords.words('french'))
    # Ajout de termes fréquents dans le secteur bancaire marocain n'apportant pas de valeur au LDA
    stop_words.update(['banque', 'cih', 'attijari', 'plus', 'tout', 'faire', 'agence', 'client'])
    
    return [t for t in tokens if t not in stop_words and len(t) > 3]

def enrich_topics():
    """
    Effectue la modélisation de thèmes (LDA) sur les avis en français.
    Le modèle se concentre sur le français car il représente la majorité (>70%) 
    du jeu de données, garantissant ainsi une pertinence statistique pour 
    l'extraction des thématiques.
    
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Extraction ciblée sur le Français (langue majoritaire pour la pertinence du modèle LDA)
    cur.execute("SELECT review_id, review_text FROM stg_enriched_reviews WHERE language = 'fr'")
    rows = cur.fetchall()
    
    if not rows:
        print("INFO: Aucun avis à traiter.")
        return

    documents = [preprocess_text(r['review_text']) for r in rows]
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]

    # Modèle LDA configuré pour identifier 5 catégories majeures
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=15, random_state=42)

    # Initialisation des colonnes de destination
    cur.execute("ALTER TABLE stg_enriched_reviews ADD COLUMN IF NOT EXISTS topic_id INTEGER;")
    cur.execute("ALTER TABLE stg_enriched_reviews ADD COLUMN IF NOT EXISTS topic_label TEXT;")

    # Mapping basé sur l'analyse de distribution des mots-clés par topic
    TOPIC_LABELS = {
        0: "Qualité Service",
        1: "Support Téléphonique",
        2: "Gestion de Compte",
        3: "Accueil Personnel",
        4: "Satisfaction Agence"
    }

    print("INFO: Mise à jour des thèmes en base de données...")
    for i, row in enumerate(rows):
        bow = corpus[i]
        topics = lda_model.get_document_topics(bow)
        dominant_topic = max(topics, key=lambda x: x[1])[0]
        label = TOPIC_LABELS.get(dominant_topic, "Autre")
        
        cur.execute(
            "UPDATE stg_enriched_reviews SET topic_id = %s, topic_label = %s WHERE review_id = %s", 
            (int(dominant_topic), label, row['review_id'])
        )

    conn.commit()
    print("SUCCESS: Enrichissement des thèmes terminé.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    enrich_topics()