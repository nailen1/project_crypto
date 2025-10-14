import os
from functools import cached_property
from canonical_transformer.morphisms import map_df_to_csv, map_csv_to_df
from universal_timeseries_transformer import transform_timeseries
from .simples import get_prices_xusdt_within_interval
from .visualizations import plot_msci_style


class SnapshotXUSDT:
    def __init__(self, interval: str = '6 hours'):
        self.file_folder = self.set_file_folder()
        self.interval = interval

    def set_file_folder(self):
        project_root = os.environ.get('PROJECT_ROOT')
        if not project_root:
            raise ValueError("PROJECT_ROOT environment variable is not set. Please check your .env file.")
        
        return os.path.join(project_root, 'data', 'snapshots')

    @cached_property
    def df(self):
        return get_prices_xusdt_within_interval(self.interval)

    @cached_property
    def file_name(self):
        latest_index = self.df.index.sort_values(ascending=False)[-1]
        file_name = f'dataset-snapshot-binance_prices_xusdt-interval{self.interval}-at{latest_index}.csv'
        return file_name

    def save(self):
        return map_df_to_csv(self.df, file_folder=self.file_folder, file_name=self.file_name)

    def load(self):
        return map_csv_to_df(file_folder=self.file_folder, file_name=self.file_name)


    @cached_property
    def btcusdt(self):
        btcusdt = transform_timeseries(self.df[['BTCUSDT']], option_type='datetime')
        return btcusdt

    def plot_btcusdt(self):
        plot_msci_style(self.btcusdt['BTCUSDT'], title=f'Binance Price.BTC/USDT.{self.interval}', ylabel='Price')