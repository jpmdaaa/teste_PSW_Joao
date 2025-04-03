from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Adiciona o caminho dos scripts ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def run_consumer():
    from consumidor_api import ConsumidorAPICervejarias
    consumidor = ConsumidorAPICervejarias()
    return consumidor.buscar_todas_cervejarias()

def run_transform():
    from transformacao import TransformadorCervejarias
    TransformadorCervejarias().processar()

with DAG(
    'cervejarias_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=run_consumer
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=run_transform
    )

    extract_task >> transform_task