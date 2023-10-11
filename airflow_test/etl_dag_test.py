import pandas as pd
import numpy as np
import requests
import json
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def _api_get_and_print_json():
    url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18/lat/59/data.json"

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the JSON data from the response
        data = response.json()
        # Now you can work with the 'data' variable, which contains the API response data

        test = pd.json_normalize(data)
        test.to_json('./etl_data/raw_data.json', orient='records', indent=4)

        print(test.head())
    else:
        # Handle the error if the request was not successful
        print(f"Request failed with status code {response.status_code}")


def _find_temperature():
    json_file_path = './etl_data/raw_data.json'
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

def _clean_time():
    json_file_path = './etl_data/temperature_data.json'
    # Read the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        
        # Use todays date
        # date_object = datetime.now().date()
        # specific_date = date_object.strftime("%Y-%m-%d")
        
        # Create a DataFrame from the collected data
        df = pd.DataFrame(json_data)
        
        # Remove the "Z" from the time column
        # df['validTime'] = df['validTime'].str.replace('Z', '')

        # # df['validTime'] = df['validTime'].str.replace(':00', '')
        # df['validTime'] = df['validTime'].str.slice(0, 5)
        # filtered_df = df[df['validDate'] == specific_date]
        
        # write json file
        df.to_json('./etl_data/cleaned_data.json', orient='records', indent=4)


def _plot_graph():
    json_file_path = './etl_data/cleaned_data.json'
    # Read the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    #Use todays date
    
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(json_data)

    # Remove the "Z" from the time column
    df['validTime'] = df['validTime'].str.replace('Z', '')
    df['validTime'] = df['validTime'].str.replace(':00', '')
    df['validTime'] = df['validTime'].str.slice(0, 5)  

    date_object = datetime.now().date()
    specific_date = date_object.strftime("%Y-%m-%d") 

    # Filter the DataFrame for a specific date (e.g., '2023-10-11')
    specific_date = '2023-10-11'

    filtered_df = df[df['validDate'] == specific_date]


    # Create a line graph for temperature
    plt.figure(figsize=(10, 6))  # Set the figure size (width, height)

    # Plot temperature data
    plt.plot(filtered_df['validTime'], filtered_df['temperature'], color= 'tab:blue')

    # Set labels and title
    plt.xlabel('Time', color = 'tab:gray', fontsize=10 )
    plt.ylabel('Temperature (°C)',  color = 'tab:gray', fontsize=10)
    plt.title(f'Temperature: {specific_date}', fontsize = 20 , color = 'tab:gray' , weight="bold")
    plt.show()
    # Save the graph as an image
    save_path = './etl_data/temperature_graph.png'
    plt.tight_layout()
    plt.savefig(save_path)






with DAG("etl_dags", start_date=datetime(2023, 10, 10), 
    schedule_interval='*/1 * * * *', catchup=False) as dag:

        api_get_and_print_json = PythonOperator(
            task_id="api_request",
            python_callable=_api_get_and_print_json
        )

        find_temperature = PythonOperator(
            task_id="find_temperature",
            python_callable=_find_temperature
        )

        clean_time = PythonOperator(
            task_id='clean_time',
            python_callable=_clean_time
        )

        plot_graph = PythonOperator(
            task_id='plot_graph',
            python_callable=_plot_graph
        )



        api_get_and_print_json >> find_temperature >> clean_time >> plot_graph
