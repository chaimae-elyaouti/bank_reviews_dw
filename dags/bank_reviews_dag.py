from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# Configuration des chemins
DAG_FOLDER = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = "/mnt/c/Users/ThinKPad/bank_reviews_dw" 
VENV_PYTHON = f"{PROJECT_PATH}/venv_linux/bin/python3" 

default_args = {
    'owner': 'chaimae_data_eng',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bank_reviews_elt_pipeline',
    default_args=default_args,
    schedule_interval='@weekly', 
    catchup=False,
) as dag:

    tache_extraction = BashOperator(
        task_id='extraire_donnees_apify',
        bash_command=f"{VENV_PYTHON} {PROJECT_PATH}/api_extractor.py",
    )

    tache_chargement = BashOperator(
        task_id='charger_donnees_postgres',
        bash_command=f"{VENV_PYTHON} {PROJECT_PATH}/load_raw.py",
    )

    tache_langue = BashOperator(
        task_id='enrichir_langue',
        bash_command=f"{VENV_PYTHON} {PROJECT_PATH}/enrich_language.py",
    )

    
    tache_topics = BashOperator(
        task_id='extraire_topics_nlp',
        bash_command=f"{VENV_PYTHON} {PROJECT_PATH}/enrich_topics.py",
    )

    tache_dbt = BashOperator(
        task_id='transformer_dbt',
        bash_command=f"cd {PROJECT_PATH}/transform_bank_reviews && dbt run",
    )
    
    tache_extraction >> tache_chargement >> tache_dbt >> tache_langue >> tache_topics