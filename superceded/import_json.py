import requests
import pandas as pd
url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18/lat/59/data.json"
response = requests.get(url)

def get_json():
    raw_data = None
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and work with the JSON data from the response
        data = response.json()
        # Now you can work with the 'data' variable, which contains the API response data

        raw_data = pd.json_normalize(data)
        raw_data.to_json('./main/raw_data.json', orient='records', indent=4)        
    else:
        # Handle the error if the request was not successful
        print(f"Request failed with status code {response.status_code}")

    return raw_data

if __name__=="__main__":
    json_df = get_json()
    if json_df is not None:
        print(json_df)

