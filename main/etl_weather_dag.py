from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from import_json import get_json
from dataframe_json import find_temperature, clean_time


with DAG("etl_project_dag", start_date=datetime(2023, 10, 10), 
    schedule_interval='*/1 * * * *', catchup=False) as dag:

        get_json = PythonOperator(
            task_id="api_request",
            python_callable=get_json
        )

        find_temperature = PythonOperator(
            task_id="find_temperature",
            python_callable=find_temperature
        )

        clean_time = PythonOperator(
            task_id='clean_time',
            python_callable=clean_time
        )


        get_json >> find_temperature >> clean_time
