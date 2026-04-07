import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2

def get_connection():
    # Détection du chemin absolu
    basedir = Path(__file__).resolve().parent
    env_path = basedir / '.env'
    load_dotenv(dotenv_path=env_path)

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")

    if not all([dbname, user, password, host]):
        raise ValueError(f"Variables manquantes dans le .env à l'adresse : {env_path}")

    return psycopg2.connect(
        host=host,
        database=dbname,
        user=user,
        password=password,
        port="5432"
    )