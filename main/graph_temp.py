# Imports dataframe_json.py to plot a temperature graph

import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
from dataframe_json import * 

# Import dataframe from dataframe_json.py
def plot_df():
    # df = df.read_json("/etl_data/raw_data.json")
    try:
        df = clean_time()
        print(df)

        # if 'validTime' in df.columns and 'temperature' in df.columns:
        #     plt.figure(figsize=(10, 6))  # Set the figure size (width, height)
        #     plt.plot(df['validTime'], df['temperature'], marker='o', linestyle='-')
        #     plt.xlabel('Time')
        #     plt.ylabel('Temperature (°C)')
        #     today = datetime.datetime.now()
        #     plt.title(f'Temperature for {today}')
        #     plt.grid(True)
        #     plt.tight_layout()
        #     plt.show()
        #else:
            # print("Data not found")
    except Exception as e:
        print(f"An error occurred: {e}")

plot_df()

# write a function to plot and save graph

