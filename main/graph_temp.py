import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime

def plot_data(input_json_file, output_file):
    
    df = pd.read_json(input_json_file)
    # Create a line graph for temperature
    plt.figure(figsize=(10, 6))  # Set the figure size (width, height)

    # Plot temperature data
    plt.plot(df['validTime'], df['temperature'], color= 'tab:blue')

    # Set labels and title
    plt.xlabel('Time', color = 'tab:gray', fontsize=10)
    plt.ylabel('Temperature (°C)',  color = 'tab:gray', fontsize=10)
    plt.title(f'Temperature {df['validDate'][0]}', fontsize = 20 , color = 'tab:gray' , weight="bold")

    # Show the graph
    plt.tight_layout()
    plt.savefig(output_file)


read_path = './etl_data/cleaned_temperature_data.json'
save_path = './etl_data/temperature_graph.png'
plot_data(read_path,save_path)