from functools import partial
import pandas as pd
from canonical_transformer.morphisms import map_df_to_csv
from .basis import get_df_by_query
from .references import (
    QUERY_PRICES_XUSDT_WITHIN_6HRS, 
    QUERY_PRICE_BTCUSDT,
    QUERY_PRICES_TEMPLATE
)

get_price_btcusdt = partial(get_df_by_query, QUERY_PRICE_BTCUSDT)


def get_prices_xusdt_within_6hrs() -> pd.DataFrame:
    df = get_df_by_query(QUERY_PRICES_XUSDT_WITHIN_6HRS)    
    df_pivot = df.pivot(index='datetime', columns='symbol', values='price')
    return df_pivot

def get_snapshot_xusdt() -> pd.DataFrame:
    df = get_prices_xusdt_within_6hrs()
    file_folder = 'data/snapshots'
    datetime_now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name=f'snapshot-binance_prices_xusdt-at{datetime_now}.csv'
    return map_df_to_csv(df, file_folder=file_folder, file_name=file_name)

def get_prices_xusdt_within_interval(interval: str) -> pd.DataFrame:
    df = get_df_by_query(QUERY_PRICES_TEMPLATE.format(interval=interval))
    df_pivot = df.pivot(index='datetime', columns='symbol', values='price')
    return df_pivot