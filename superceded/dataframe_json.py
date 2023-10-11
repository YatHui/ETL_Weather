import pandas as pd
import json
from datetime import datetime

def find_temperature():
    json_file_path = './main/raw_data.json'
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
    

def clean_time():
    json_file_path = './etl_data/temperature_data.json'
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


if __name__=="__main__":
    find_temperature()
    test = clean_time()
    print(test)
