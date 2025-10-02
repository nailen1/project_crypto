import pandas as pd
import requests
from canonical_transformer.morphisms import map_df_to_csv
from crypto_etl.path_director import FILE_FOLDER
from .consts import BINANCE_API_URL


def fetch_data_binance_at_present()->tuple[requests.Response, pd.Timestamp]:    
    url = BINANCE_API_URL
    response = requests.get(url)
    datetime = pd.Timestamp.now()
    return response, datetime


def style_df_at_present(df:pd.DataFrame, datetime:pd.Timestamp)->pd.DataFrame:
    SYMBOL_COLUMN_NAME = 'symbol'
    df = df.set_index(SYMBOL_COLUMN_NAME)
    df.columns = [datetime]
    df.index.name = None
    df = df.T
    INDEX_NAME_FOR_DATETIME = 'datetime'
    df.index.name = INDEX_NAME_FOR_DATETIME
    return df


def get_df_binance_at_present()->pd.DataFrame:
    response, datetime = fetch_data_binance_at_present()
    if response.status_code == 200:
        data_price = response.json()
        df_at_present = pd.DataFrame(data_price)
        df_at_present = style_df_at_present(df_at_present, datetime)
        return df_at_present
    else:
        return None


def save_df_binance_at_present()->pd.DataFrame:
    df_at_present = get_df_binance_at_present()
    if df_at_present is not None:
        datetime_at_present = df_at_present.index[0]
        df_at_present.index = df_at_present.index.strftime('%Y-%m-%d %H:%M:%S')
        return map_df_to_csv(df_at_present, file_folder=FILE_FOLDER['binance'], file_name=f'binance_api-at{datetime_at_present}.csv')
    else:
        print("Failed to fetch data from Binance")
