from functools import cached_property
import os
from universal_timeseries_transformer import transform_timeseries
from shining_pebbles import check_folder_and_create_folder
from canonical_transformer.morphisms import map_df_to_data, map_data_to_json
from .simples import get_two_points_by_time_diff
from .consts import FILE_FOLDER_CACHE

class Momentum:
    def __init__(self, time_diff, time_unit, symbol_refrence=None, batch_size=10, option_dropna=True):
        self.time_diff = time_diff
        self.time_unit = time_unit
        self.symbol_refrence = symbol_refrence
        self.batch_size = batch_size
        self.option_dropna = option_dropna

    @cached_property
    def points(self):
        df = get_two_points_by_time_diff(self.time_diff, self.time_unit)
        if self.symbol_refrence:
            df = df.filter(regex=f'{self.symbol_refrence}$')
        return df

    @cached_property
    def t_i(self):
        return self.points.index[0]

    @cached_property
    def t_f(self):
        return self.points.index[-1]

    @cached_property
    def points_with_datetime(self):
        return transform_timeseries(self.points, option_type='datetime')

    @cached_property
    def datetime_i(self):
        return self.points_with_datetime.index[0]

    @cached_property
    def datetime_f(self):
        return self.points_with_datetime.index[-1]

    @cached_property
    def exact_time_diff(self):
        return self.datetime_f - self.datetime_i

    def calculate(self):
        df = self.points.T

        def style_df(df):
            col_name_momentum = f'momentum: {self.time_diff} {self.time_unit}'
            df[col_name_momentum] = (df.iloc[:, 1] / df.iloc[:, 0] - 1) * 100
            if self.option_dropna:
                df = df.dropna()
            df = df.sort_values(by=col_name_momentum, ascending=False)
            df.columns.name = None
            df.index.name = 'symbol'
            return df

        return style_df(df)

    @cached_property
    def details(self):
        print(f'exact time diff: {self.exact_time_diff}')
        print(f'datetime i: {self.datetime_i}')
        print(f'datetime f: {self.datetime_f}')
        return self.calculate()

    @cached_property
    def momentum(self):
        return self.calculate().iloc[:, [-1]]

    @cached_property
    def rank(self):
        df = self.momentum.reset_index()
        df['rank'] = df.index
        df = df[['symbol', 'rank']].set_index('symbol')
        return df

    @cached_property
    def momentum_with_rank(self):
        df = self.momentum.reset_index()
        df.index.name = 'rank'
        return df

    def get_tops(self, batch_size=None):
        batch_size = batch_size if batch_size else self.batch_size
        return self.momentum.head(self.batch_size)

    def get_bottoms(self, batch_size=None):
        batch_size = batch_size if batch_size else self.batch_size
        return self.momentum.tail(self.batch_size)

    @cached_property
    def tops(self):
        return self.get_tops()

    @cached_property
    def bottoms(self):
        return self.get_bottoms()

    @cached_property
    def row_btc(self):
        if self.symbol_refrence != 'BTC' or self.symbol_refrence is None:
            df = self.momentum_with_rank
            row = df[df['symbol'] == f'BTC{self.symbol_refrence}']
            return row
        else:
            raise ValueError(f'symbol_refrence must be not BTC itself or None, but {self.symbol_refrence}')

    @cached_property
    def metadata(self):
        return {
            'symbol': self.symbol_refrence,
            'time_diff': self.time_diff,
            'time_unit': self.time_unit,
            'exact_time_diff': self.exact_time_diff,
            'datetime_i': self.datetime_i,
            'datetime_f': self.datetime_f,
            'time_diff': self.time_diff,
            'time_unit': self.time_unit,
            'symbol_refrence': self.symbol_refrence,
            'batch_size': self.batch_size,
        }

    @cached_property
    def api__data__momentum(self):
        return map_df_to_data(self.momentum)

    @cached_property
    def api__data(self, option_save_json=True):
        data =map_df_to_data(self.momentum_with_rank)
        if option_save_json:
            file_folder = FILE_FOLDER_CACHE        
            check_folder_and_create_folder(file_folder)
            map_data_to_json(data=data, file_folder=file_folder, file_name=f'json-momentum-{self.symbol_refrence}-{self.time_diff}-{self.time_unit}.json')
        return data

    @cached_property
    def api__data__row_btc(self):
        return map_df_to_data(self.row_btc)

    @cached_property
    def api_metadata(self):
        return map_df_to_data(self.metadata)