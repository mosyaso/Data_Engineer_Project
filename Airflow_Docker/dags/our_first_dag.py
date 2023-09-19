from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'syakir1937',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
with DAG(
    dag_id='our_first_dag_v5',
    default_args=default_args,
    description='This is our first dag that syakir write',
    start_date=datetime(2023, 9, 16, 2), #run in 16 sept 2023 at 2am
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is the first task!"
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo hey, I am task2 and will be running after task1"
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo hey, I am task3 and will be running after task1"
    )

    #Task dependency method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    #Task dependency method 2
    # task1 >> task2
    # task1 >> task3

    #Task dependency method 3
    task1 >> [task2, task3]
