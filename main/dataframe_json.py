import pandas as pd
import json
import matplotlib.pyplot as plt

json_file_path = './main/raw_json.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Create an empty list to store the data
data = []