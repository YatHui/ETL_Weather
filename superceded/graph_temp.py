import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime

def plot_data(input_json_path, value, output_path):
    
    df = pd.read_json(input_json_path)
    date_object = datetime.now().date()
    specific_date = date_object.strftime("%Y-%m-%d") 

    # Filter the DataFrame for a specific date (e.g., '2023-10-11')
    
    filtered_df = df[df['validDate'] == specific_date]


    # Create a line graph for temperature
    plt.figure(figsize=(10, 6))  # Set the figure size (width, height)

    # Plot temperature data
    plt.scatter(filtered_df['validTime'], filtered_df[value], color= 'tab:blue')

    # Set labels and title
    plt.xlabel('Time', color = 'tab:gray', fontsize=10 )
    plt.ylabel(f'{value}',  color = 'tab:gray', fontsize=10)
    plt.title(f'{value}: {specific_date}', fontsize = 20 , color = 'tab:gray' , weight="bold")
    # Save the graph as an image
    # save_path = './etl_data/temperature_graph.png'
    plt.tight_layout()
    plt.savefig(output_path)


read_path = './etl_data/cleaned_temperature_data.json'
save_path = './etl_data/temperature_graph.png'
plot_data(read_path, 'temperature', save_path)
read_path2 = './etl_data/cleaned_humidity_data.json'
save_path2 = './etl_data/humidity_graph.png'
plot_data(read_path2, 'humidity', save_path2)