import time
from .utils import save_df_binance_at_present

TIME_INTERVAL_SECONDS = 10

def run_scheduler(time_interval_seconds:int=TIME_INTERVAL_SECONDS):
    """Run Binance data collection scheduler."""
    print("Starting Binance data collection scheduler...")
    try:
        while True:
            try:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting data collection")
                save_df_binance_at_present()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data collection completed")
            except Exception as e:
                print(f"Error occurred: {e}")
            
            # Wait 10 seconds before next collection
            time.sleep(time_interval_seconds)
    except KeyboardInterrupt:
        print("\nScheduler stopped")

if __name__ == "__main__":
    run_scheduler()