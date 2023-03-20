import numpy as np
import pandas as pd
import requests
import streamlit as st

headers = {'Accept': 'application/json'}

api_url = ""
beers_url = "beers"

def make_request(main_url, service_url):
    response = requests.get(f"{main_url}{service_url}", headers = headers)
    #print(f"Response: {r.json()}")
    response_json = response.json()
    return response_json

def load_json_to_dataframe(response_json):
    target_json = response_json["result"]
    try:
        df = pd.json_normalize(target_json)
    except Exception as e:
        print(e)
    return df 

def load_data(main_url, service_URL):
    response_json = make_request(api_url, beers_url)
    df = load_json_to_dataframe(response_json)
    return response_json, df

response_json, beers_df = load_data(api_url, beers_url)
#print(beers_df.info())

st.json(response_json)
st.dataframe(beers_df)