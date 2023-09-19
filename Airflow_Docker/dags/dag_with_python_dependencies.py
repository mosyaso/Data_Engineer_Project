from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'syakir1937',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_sklearn():
    import sklearn
    print(f"scikit-learn with version: {sklearn.__version__}")

with DAG(
    dag_id='dag_with_postgres_operator_v03',
    default_args=default_args,
    start_date=datetime(2023, 9, 16, 2), #run in 16 sept 2023 at 2am
    schedule_interval='0 0 * * *'
) as dag:
    
    get_sklearn= PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn
    )

    get_sklearn