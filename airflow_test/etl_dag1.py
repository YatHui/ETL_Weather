import pandas as pd
import numpy as np
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def _api_request():
    url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18/lat/59/data.json"

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the JSON data from the response
        data = response.json()
        # Now you can work with the 'data' variable, which contains the API response data

        test = pd.json_normalize(data)
        test.to_json('./test.json', orient='records', indent=4)

        print(test.head())
    else:
        # Handle the error if the request was not successful
        print(f"Request failed with status code {response.status_code}")


with DAG("etl_project_dag", start_date=datetime(2023, 10, 10), 
    schedule_interval='*/1 * * * *', catchup=False) as dag:

        load_json_and_separate = PythonOperator(
            task_id="api_request",
            python_callable=_api_request
        )

