from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def run_consumer():
    import sys
    sys.path.append('/opt/airflow/scripts')
    from consumidor_api import ConsumidorAPICervejarias
    consumidor = ConsumidorAPICervejarias()
    return consumidor.buscar_todas_cervejarias()

def run_transform(data):
    from transformacao import TransformadorCervejarias
    TransformadorCervejarias().processar(data)

with DAG(
    'cervejarias_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['brewery']
) as dag:

    start = DummyOperator(task_id='start')

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=run_consumer,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=run_transform,
        op_args=["{{ ti.xcom_pull(task_ids='extract_data') }}"]
    )

    end = DummyOperator(task_id='end')

    start >> extract_task >> transform_task >> end