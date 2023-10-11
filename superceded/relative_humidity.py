import json
import pandas as pd
from datetime import datetime


def find_humidity():
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
            if param['name'] == 'r':
                humidity = param['values'][0]
                date, time = valid_time.split('T')
                data.append({'validDate': date, 'validTime': time, 'humidity': humidity})
    
    df = pd.DataFrame(data)
    
    #Use todays date for the streamlined file
    date_object = datetime.now().date()
    specific_date = date_object.strftime("%Y-%m-%d")

    # Remove the "Z" from the time column
    df['validTime'] = df['validTime'].str.replace('Z', '')

    df['validTime'] = df['validTime'].str.slice(0, 5)
    filtered_df = df[df['validDate'] == specific_date]
    
    # write json file
    filtered_df.to_json('./etl_data/humidity_data.json', orient='records', indent=4)


find_humidity()