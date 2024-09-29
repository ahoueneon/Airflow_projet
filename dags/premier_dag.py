from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.email import EmailOperator  # Ajusté l'importation  
from mes_fonctions import generer_fichier 

def dire_bonjour():
        print("bonjour, c'est fait")

def print_python_path():
    import sys
    print(f"Python path: {sys.executable}")

default_args = {
    'owner': 'Gohou Christian',
    'depends_on_past': True, 
    'start_date': datetime(2024, 9, 26), 
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Définir le DAG
with DAG( 
    'Donnees_Generees',
    default_args=default_args,
    description='DAG modulaire avec des fonctions séparées',
    schedule_interval='0 4 * * *',
    catchup=False,
) as dag:

    tache_traitement = PythonOperator(
        task_id='generer_fichiers_journaliers',  # Corrigé : pas d'espaces
        python_callable=generer_fichier,
    )

    print_path_task = PythonOperator(
    task_id='print_python_path',
    python_callable=print_python_path,
    )

    

    # tache_envoyer_email = EmailOperator(
    #     task_id='envoyer_email',  # Corrigé : pas d'espaces
    #     to='gohouchristian35@gmail.com',
    #     subject="Informations sur l'état des rapports",
    #     html_content='<p>Les rapports du jour ont été actualisés. Vous pouvez le consulter <a href="URL_DU_RAPPORT">ici</a>.</p>',
    # )

    # Orchestration des tâches
    tache_traitement >> print_path_task 
