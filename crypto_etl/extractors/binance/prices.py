"""
Binance prices data extractor module.

This module provides functions to fetch and process current price data from Binance API.
"""
import pandas as pd
import requests
from canonical_transformer.morphisms import map_df_to_csv, map_df_to_data
from crypto_database.postgres.insert import insert_binance_prices
from crypto_etl.path_director import FILE_FOLDER
from .consts import BINANCE_API_PRICE


def fetch_data_binance_prices_at_present() -> tuple[requests.Response, pd.Timestamp]:
    """
    Fetch current price data from Binance API.

    Returns:
        tuple: (response object, current timestamp)
    """
    url = BINANCE_API_PRICE
    response = requests.get(url, timeout=10)
    datetime = pd.Timestamp.now()
    return response, datetime


def style_df_binance_prices_at_present(df: pd.DataFrame, datetime: pd.Timestamp) -> pd.DataFrame:
    """
    Style the DataFrame for current price data.

    Args:
        df: Raw price DataFrame
        datetime: Current timestamp

    Returns:
        pd.DataFrame: Styled DataFrame with datetime index
    """
    symbol_column_name = 'symbol'
    df = df.set_index(symbol_column_name)
    df.columns = [datetime]
    df.index.name = None
    df = df.T
    index_name_for_datetime = 'datetime'
    df.index.name = index_name_for_datetime
    return df


def get_df_binance_prices_at_present() -> pd.DataFrame:
    """
    Get current Binance price data as DataFrame.

    Returns:
        pd.DataFrame: Current price data or None if failed
    """
    try:
        response, datetime = fetch_data_binance_prices_at_present()
        if response.status_code == 200:
            data_price = response.json()
            df_at_present = pd.DataFrame(data_price)
            df_at_present = style_df_binance_prices_at_present(df_at_present, datetime)
            return df_at_present
        print(f"API error: {response.status_code}")
        return None
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching data: {e}")
        return None


def insert_and_save_df_binance_prices_at_present(
    option_insert: bool = True,
    option_save: bool = True
) -> pd.DataFrame:
    """
    Insert and save current Binance price data.

    Args:
        option_insert: Whether to insert data into database
        option_save: Whether to save data to CSV file

    Returns:
        pd.DataFrame: Price data or None if failed
    """
    df_at_present = get_df_binance_prices_at_present()

    if df_at_present is None:
        print("Failed to fetch data from Binance")
        return None

    try:
        # INSERT
        if option_insert:
            print("Inserting data into schema_crypto.binance_prices")
            data_at_present = map_df_to_data(df_at_present)
            result = insert_binance_prices(
                data=data_at_present,
                table_name='schema_crypto.binance_prices'
            )
            print(f"✓ Inserted: {result['inserted']}, "
                  f"Skipped: {result['skipped']}, "
                  f"Failed: {result['failed']}")
            del data_at_present

        # CSV 저장
        if option_save:
            print(f"Saving df into {FILE_FOLDER['binance-prices']}")
            datetime_at_present = df_at_present.index[0]
            df_for_csv = df_at_present.copy()
            df_for_csv.index = df_for_csv.index.strftime('%Y-%m-%d %H:%M:%S')
            map_df_to_csv(
                df_for_csv,
                file_folder=FILE_FOLDER['binance-prices'],
                file_name=f'binance_prices-at{datetime_at_present}.csv'
            )
            del df_for_csv

        return df_at_present

    except (KeyError, ValueError, OSError) as e:
        print(f"Error in insert_and_save: {e}")
        return None

def save_df_binance_prices_at_present():
    """
    Save current Binance price data to CSV file.
    """
    insert_and_save_df_binance_prices_at_present(option_insert=False, option_save=True)