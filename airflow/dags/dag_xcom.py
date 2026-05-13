from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries':3,
    'retry_delay': timedelta(minutes=5)
}

def transform_log(ti):
    event_log = {
        'attach': 'It was proccessed 100 logs',
        'l_handover': 'It was proccessed 50 logs',
        'service_request': 'It was proccessed 20 logs'
    }

    [ti.xcom_push(key=key, value=value) for key, value in event_log.items()]

def logs_menu(ti):
    attach = ti.xcom_pull(task_ids='transform_log',key='attach')
    l_handover = ti.xcom_pull(task_ids='transform_log',key='l_handover')
    service_request = ti.xcom_pull(task_ids='transform_log',key='service_request')
    message = f"""Logs processed:
- Attach: {attach}
- L_Handover: {l_handover}
- Service Request: {service_request}
"""
    print(message)

with DAG(
    default_args=default_args,
    dag_id='dag_xcom',
    description='A simple DAG to demonstrate XComs',
    start_date=datetime(2025, 3, 6, 2),
    schedule='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='transform_log',
        python_callable=transform_log,
    )
    task2 = PythonOperator(
        task_id='logs_menu',
        python_callable=logs_menu,
    )

    task1 >> task2