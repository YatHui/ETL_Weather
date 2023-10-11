from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import requests
import pandas as pd
# import matplotlib.pyplot as plt

url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18/lat/59/data.json"
response = requests.get(url)

def _get_json():
    raw_data = None
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the JSON data from the response
        data = response.json()
        # Now you can work with the 'data' variable, which contains the API response data

        raw_data = pd.json_normalize(data)
        raw_data.to_json('./etl_data/raw_data.json', orient='records', indent=4)        
    else:
        # Handle the error if the request was not successful
        print(f"Request failed with status code {response.status_code}")

    return raw_data

def _clean_time():
    json_file_path = './etl_data/raw_data.json'
    # Read the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        
        #Use todays date
        date_object = datetime.now().date()
        specific_date = date_object.strftime("%Y-%m-%d")
        
        # Create a DataFrame from the collected data
        df = pd.DataFrame(json_data)
        
        # Remove the "Z" from the time column
        df['validTime'] = df['validTime'].str.replace('Z', '')

        # df['validTime'] = df['validTime'].str.replace(':00', '')
        df['validTime'] = df['validTime'].str.slice(0, 5)
        filtered_df = df[df['validDate'] == specific_date]
        
        # write json file
        filtered_df.to_json('./etl_data/cleaned_data.json', orient='records', indent=4)

def _find_temperature():
    json_file_path = './etl_data/cleaned_data.json'
    # Read the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Create an empty list to store the data
    data = []
    # Itirate through timeseries-data
    for series in json_data[0]['timeSeries']:
        valid_time = series['validTime']
        parameters = series['parameters']
        for param in parameters:
            if param['name'] == 't':
                temperature = param['values'][0]
                date, time = valid_time.split('T')
                data.append({'validDate': date, 'validTime': time, 'temperature': temperature})
    
    df = pd.DataFrame(data)
    # write json file
    df.to_json('./etl_data/temperature_data.json', orient='records', indent=4)

with DAG("etl_project_dag", start_date=datetime(2023, 10, 10), 
    schedule_interval='*/1 * * * *', catchup=False) as dag:

        get_json = PythonOperator(
            task_id="api_request",
            python_callable=_get_json
        )

        clean_time = PythonOperator(
            task_id='clean_time',
            python_callable=_clean_time
        )

        find_temperature = PythonOperator(
            task_id="find_temperature",
            python_callable=_find_temperature
        )


        get_json >> clean_time >> find_temperature