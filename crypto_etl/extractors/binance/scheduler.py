import time
from .utils import insert_and_save_df_binance_at_present


def run_scheduler(time_interval_seconds:int):
    """Run Binance data collection scheduler."""
    print("Starting Binance data collection scheduler...")
    try:
        while True:
            try:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting data collection")
                insert_and_save_df_binance_at_present()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data collection completed")
            except Exception as e:
                print(f"Error occurred: {e}")
            
            # Wait 10 seconds before next collection
            time.sleep(time_interval_seconds)
    except KeyboardInterrupt:
        print("\nScheduler stopped")