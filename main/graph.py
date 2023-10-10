import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
from dataframe_json import *

# Import dataframe from dataframe_json.py

def plot_df():
    # df = df.read_json("/etl_data/raw_data.json")
    df = clean_time()

print(df)