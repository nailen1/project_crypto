from functools import reduce
from datetime import datetime, timedelta
from shining_pebbles import scan_files_including_regex, load_csv_in_file_folder_by_regex
from .consts import FILE_FOLDER_BINANCE


def scan_binance_folder(regex=''):
    file_names = scan_files_including_regex(
        file_folder=FILE_FOLDER_BINANCE,
        regex=regex
    )
    return file_names

def extract_datetimes_in_binance_folder():
    file_names = scan_binance_folder()
    datetimes = [file_name.split('-at')[-1].split('.csv')[0] for file_name in file_names]
    return datetimes

def calculate_datepoints(time_diff, time_unit='minutes'):
    now = datetime.now()
    datetime_now = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Calculate past datetime based on time unit
    if time_unit == 'minutes':
        datetime_past = (now - timedelta(minutes=time_diff)).strftime('%Y-%m-%d %H:%M:%S')
    elif time_unit == 'hours':
        datetime_past = (now - timedelta(hours=time_diff)).strftime('%Y-%m-%d %H:%M:%S')
    elif time_unit == 'days':
        datetime_past = (now - timedelta(days=time_diff)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise ValueError(f"Unsupported time_unit: {time_unit}")
    
    # Extract datetimes and find the latest one before past datetime
    datetimes = extract_datetimes_in_binance_folder()
    datetime_latest = [datetime for datetime in datetimes if datetime <= datetime_now][-1]
    datetime_past = [datetime for datetime in datetimes if datetime <= datetime_past][-1]
    
    return datetime_past, datetime_latest


def load_binance_file(file_name):
    df = load_csv_in_file_folder_by_regex(
        file_folder=FILE_FOLDER_BINANCE,
        regex=file_name
    )
    return df

def merge_binance_files(file_names):
    dfs = [load_binance_file(file_name) for file_name in file_names]
    df = reduce(lambda x, y: x.T.join(y.T, how='outer').T, dfs).sort_index()
    return df

def get_two_pints_by_regex(regex):
    file_names = scan_binance_folder(regex=regex)
    two_points = merge_binance_files(file_names)
    return two_points

def get_two_points_by_time_diff(time_diff, time_unit):
    latest, past = calculate_datepoints(time_diff, time_unit)
    regex = f'{past}|{latest}'
    return get_two_pints_by_regex(regex)
