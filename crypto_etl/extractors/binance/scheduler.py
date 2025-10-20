import time
from .prices import insert_and_save_df_binance_prices_at_present, save_df_binance_prices_at_present
from .klines import insert_and_save_df_binance_klines_5m, save_df_binance_klines_5m


def run_prices_scheduler(time_interval_seconds:int):
    """Run Binance prices data collection scheduler."""
    print("Starting Binance data collection scheduler...")
    try:
        while True:
            try:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting data collection")
                insert_and_save_df_binance_prices_at_present()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data collection completed")
            except Exception as e:
                print(f"Error occurred: {e}")
            
            # Wait 10 seconds before next collection
            time.sleep(time_interval_seconds)
    except KeyboardInterrupt:
        print("\nScheduler stopped")

def run_klines_scheduler(time_interval_seconds:int):
    """Run Binance klines data collection scheduler."""
    print("Starting Binance data collection scheduler...")
    try:
        while True:
            try:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting data collection")
                insert_and_save_df_binance_klines_5m()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data collection completed")
            except Exception as e:
                print(f"Error occurred: {e}")
            # Wait 10 seconds before next collection
            time.sleep(time_interval_seconds)
    except KeyboardInterrupt:
        print("\nScheduler stopped")