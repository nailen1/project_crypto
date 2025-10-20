"""
Binance K-lines data extractor module.

This module provides functions to fetch and process K-line data from Binance API.
"""
import concurrent.futures
import requests
import pandas as pd
from canonical_transformer.morphisms import map_df_to_csv, map_df_to_data
from crypto_database.postgres.insert import insert_binance_klines
from crypto_etl.path_director import FILE_FOLDER
from .consts import BINANCE_API_KLINES, BINANCE_API_PRICE


def fetch_binance_single_kline(symbol, time_interval: str):
    """
    Fetch single kline data from Binance API.

    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
        time_interval: Time interval ('1m', '5m', '15m', '30m', '1h', '4h', '1d')

    Returns:
        dict: K-line data or None if failed
    """
    if time_interval not in ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]:
        raise ValueError(f"Invalid time interval: {time_interval}")

    try:
        params = {
            "symbol": symbol,
            "interval": time_interval,
            "limit": 1
        }
        response = requests.get(BINANCE_API_KLINES, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            return {
                "symbol": symbol,
                "datetime_open": pd.Timestamp(data[0], unit='ms'),
                "datetime_close": pd.Timestamp(data[6], unit='ms'),
                "open": float(data[1]),
                "high": float(data[2]),
                "low": float(data[3]),
                "close": float(data[4]),
                "volume": float(data[5]),
                "quote_volume": float(data[7]),
                "trades_count": int(data[8]),
                "taker_buy_volume": float(data[9]),
                "taker_buy_quote_volume": float(data[10])
            }
    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"Error fetching {symbol}: {e}")
    return None


def fetch_binance_klines_5m_parallel():
    """
    Fetch 5-minute kline data for all symbols in parallel.

    Returns:
        list: List of kline data dictionaries
    """
    # All symbols list
    response = requests.get(BINANCE_API_PRICE, timeout=10)
    symbols = [item['symbol'] for item in response.json()]

    results = []

    # Parallel processing (50 concurrent requests)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(fetch_binance_single_kline, symbol, "5m")
                   for symbol in symbols]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results


def get_df_binance_klines_5m():
    """
    Get 5-minute kline data as DataFrame.

    Returns:
        pd.DataFrame: K-line data with symbol as index
    """
    data = fetch_binance_klines_5m_parallel()
    df = pd.DataFrame(data).set_index('symbol')
    return df


def insert_and_save_df_binance_klines_5m(option_insert: bool = True,
                                         option_save: bool = True):
    """
    Insert and save 5-minute kline data.

    Args:
        option_insert: Whether to insert data into database
        option_save: Whether to save data to CSV file

    Returns:
        pd.DataFrame: K-line data
    """
    df = get_df_binance_klines_5m()
    if df is None:
        print("Failed to fetch data from Binance")
        return None

    if option_insert:
        print("Inserting data into schema_crypto.binance_klines")
        data_klines = map_df_to_data(df)
        result = insert_binance_klines(
            data=data_klines,
            table_name='schema_crypto.binance_klines'
        )
        print(f"✓ Inserted: {result['inserted']}, "
              f"Skipped: {result['skipped']}, "
              f"Failed: {result['failed']}")
        del data_klines

    if option_save:
        print(f"Saving df into {FILE_FOLDER['binance-klines']}")
        datetime_close = str(df['datetime_close'].max())
        df_for_csv = df.copy()
        map_df_to_csv(df_for_csv,
                      file_folder=FILE_FOLDER['binance-klines'],
                      file_name=f'binance_klines_5m-at{datetime_close}.csv')
        del df_for_csv

    return df


def save_df_binance_klines_5m():
    """
    Save 5-minute kline data (insert to DB and save to CSV).
    """
    insert_and_save_df_binance_klines_5m(option_insert=False, option_save=True)
