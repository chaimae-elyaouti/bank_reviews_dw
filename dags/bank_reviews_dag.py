from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bank_reviews_elt_pipeline',
    default_args=default_args,
    description='Pipeline ELT pour extraire et charger les avis bancaires marocains',
    schedule_interval='@weekly', 
    catchup=False,
) as dag:
    
    PROJECT_PATH = "/mnt/c/Users/ThinKPad/bank_reviews_dw"

    
    tache_extraction = BashOperator(
        task_id='extraire_donnees_apify',
        bash_command=f"cd {PROJECT_PATH} && {PROJECT_PATH}/venv/Scripts/python.exe api_extractor.py",
    )

    tache_chargement = BashOperator(
        task_id='charger_donnees_postgres',
        bash_command=f"cd {PROJECT_PATH} && {PROJECT_PATH}/venv/Scripts/python.exe load_raw.py",
    )

    tache_extraction >> tache_chargement