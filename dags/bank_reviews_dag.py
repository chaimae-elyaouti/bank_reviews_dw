import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuration dynamique du chemin (Propre pour GitHub)
DAG_FOLDER = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(DAG_FOLDER, '..'))
PYTHON_EXEC = "python3" 

default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2023, 1, 1),
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
        bash_command=f"cd {PROJECT_PATH} && python3 api_extractor.py",
    )

    tache_chargement = BashOperator(
        task_id='charger_donnees_postgres',
        bash_command=f"cd {PROJECT_PATH} && python3 load_raw.py",
    )

    tache_langue = BashOperator(
        task_id='enrichir_langue',
        bash_command=f"cd {PROJECT_PATH} && python3 enrich_language.py",
    )

    tache_dbt = BashOperator(
        task_id='transformer_dbt',
        bash_command=f"cd {PROJECT_PATH}/transform_bank_reviews && dbt run",
    )

    tache_extraction >> tache_chargement >> tache_langue >> tache_dbt