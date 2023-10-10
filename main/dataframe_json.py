import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime 

json_file_path = './main/raw_data.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Create an empty list to store the data
data = []

def find_temperature(json_data):
    # Itirate through timeseries-data
    for series in json_data[0]['timeSeries']:
        valid_time = series['validTime']
        parameters = series['parameters']
        for param in parameters:
            if param['name'] == 't':
                temperature = param['values'][0]
                date, time = valid_time.split('T')
                data.append({'validDate': date, 'validTime': time, 'temperature': temperature})



def clean_time(data):
    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    # Remove the "Z" from the time column
    df['validTime'] = df['validTime'].str.replace('Z', '')

    # df['validTime'] = df['validTime'].str.replace(':00', '')
    df['validTime'] = df['validTime'].str.slice(0, 5)
    return df

today = datetime.datetime.now()

find_temperature(json_data)
test = clean_time(data)
print(test)
print(today)