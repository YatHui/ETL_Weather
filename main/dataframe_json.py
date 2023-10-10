import pandas as pd
import json
import matplotlib.pyplot as plt

json_file_path = './main/raw_json.json'

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path)

# Create an empty list to store the data
data = []