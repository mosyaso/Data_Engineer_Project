from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'syakir1937',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_catchup_backfill_v01',
    default_args=default_args,
    description='This is our first dag that syakir write',
    start_date=datetime(2023, 9, 16, 2), #run in 16 sept 2023 at 2am
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command!'
    )