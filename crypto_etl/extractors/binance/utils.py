import pandas as pd
import requests
from canonical_transformer.morphisms import map_df_to_csv, map_df_to_data
from crypto_etl.database_manager.postgres_manager.insert import insert_binance_data
from crypto_etl.path_director import FILE_FOLDER
from .consts import BINANCE_API_URL


def fetch_data_binance_at_present() -> tuple[requests.Response, pd.Timestamp]:    
    url = BINANCE_API_URL
    response = requests.get(url, timeout=10)
    datetime = pd.Timestamp.now()
    return response, datetime


def style_df_at_present(df: pd.DataFrame, datetime: pd.Timestamp) -> pd.DataFrame:
    SYMBOL_COLUMN_NAME = 'symbol'
    df = df.set_index(SYMBOL_COLUMN_NAME)
    df.columns = [datetime]
    df.index.name = None
    df = df.T
    INDEX_NAME_FOR_DATETIME = 'datetime'
    df.index.name = INDEX_NAME_FOR_DATETIME
    return df


def get_df_binance_at_present() -> pd.DataFrame:
    try:
        response, datetime = fetch_data_binance_at_present()
        if response.status_code == 200:
            data_price = response.json()
            df_at_present = pd.DataFrame(data_price)
            df_at_present = style_df_at_present(df_at_present, datetime)
            return df_at_present
        else:
            print(f"API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def insert_and_save_df_binance_at_present(
    option_insert: bool = True, 
    option_save: bool = True
) -> pd.DataFrame:
    df_at_present = get_df_binance_at_present()
    
    if df_at_present is None:
        print("Failed to fetch data from Binance")
        return None
    
    try:
        # INSERT
        if option_insert:
            print(f"Inserting data into schema_crypto.prices_binance")
            data_at_present = map_df_to_data(df_at_present)
            result = insert_binance_data(
                data=data_at_present, 
                table_name='schema_crypto.prices_binance'
            )
            print(f"✓ Inserted: {result['inserted']}, Skipped: {result['skipped']}, Failed: {result['failed']}")
            del data_at_present
        
        # CSV 저장
        if option_save:
            print(f"Saving df into {FILE_FOLDER['binance']}")
            datetime_at_present = df_at_present.index[0]
            df_for_csv = df_at_present.copy()
            df_for_csv.index = df_for_csv.index.strftime('%Y-%m-%d %H:%M:%S')
            map_df_to_csv(
                df_for_csv, 
                file_folder=FILE_FOLDER['binance'], 
                file_name=f'binance_api-at{datetime_at_present}.csv'
            )
            del df_for_csv
        
        return df_at_present
        
    except Exception as e:
        print(f"Error in insert_and_save: {e}")
        return None