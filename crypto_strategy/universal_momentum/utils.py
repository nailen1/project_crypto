import pandas as pd
from timeseries_performance_calculator import Performance
from crypto_database.applications.classes import SnapshotXUSDT


def get_prices_6hr() -> pd.DataFrame:   
    snapshot_xusdt = SnapshotXUSDT()
    prices = snapshot_xusdt.df
    return prices


def get_momentum_6hr() -> pd.DataFrame:
    prices = get_prices_6hr()

    def style_momentum_6hr() -> pd.DataFrame:
        perf = Performance(timeseries=prices)
        df = perf.cumreturns.iloc[[-1], :].T
        df.index = [idx.replace('cumreturn: ', '') for idx in df.index]
        df.index.name = 'symbol'
        df.columns = ['momentum: 6hr']
        df.sort_values(by='momentum: 6hr', ascending=False, inplace=True)
        return df

    return style_momentum_6hr()