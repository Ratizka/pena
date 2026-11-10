import os
from pathlib import Path

import requests
import pandas as pd

def haeData(url):
    try:
        response = requests.get(url, timeout=240)
        return response.json()
    except requests.RequestException as e:
        print(f"Virhe datan haussa: {e}")


def normalisoi(data):
    return pd.json_normalize(data['players'])


def modify(data):
    # Todellinen heittoprosentti NBA määritelmällä
    data['ts'] = data['total_points'] / \
        (2 * (data['total_fga'] + 0.44 * data['total_fta']))
        
    data['eFG'] = (data['total_fgm']+(0.5*data['total_s_3m'])) / \
        data['total_fga']
    
    return data


def tallennaCSV(df):
    df.to_csv(
        f"{Path(__file__).parent.parent.resolve()}/data/pelaajadata.csv", index=False)
    

def main():
    response = haeData(
        "https://basket.fi/wp-json/basket/v1/pena-api/api/v1/competitions/f874dc00-e92f-5090-beb3-e47826cda185/seasons/9c18e5ca-76f9-5294-ac23-aa9b22f5ab01/statistics/players")
    
    normData = normalisoi(response)
    
    data = modify(normData)
    
    tallennaCSV(data)

if __name__ == "__main__":
    main()
