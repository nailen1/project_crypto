#!/usr/bin/env python3
"""
Crypto ETL - Main Entry Point
=============================

Main execution script for the Crypto ETL system.
This script runs the Binance cryptocurrency data collection scheduler.

Usage:
    python main.py
    ./main.py

Features:
    - Automatic data collection every 10 seconds
    - Error handling and recovery
    - Timestamp logging
    - Graceful shutdown with Ctrl+C

Author: Crypto ETL Team
Version: 1.0.0
"""

import time
import threading
from crypto_etl.extractors.binance.scheduler import run_prices_scheduler, run_klines_scheduler

TIME_INTERVAL_SECONDS_FOR_PRICES = 10
TIME_INTERVAL_SECONDS_FOR_KLINES = 300

if __name__ == "__main__":
    # Create threads for both schedulers
    prices_thread = threading.Thread(
        target=run_prices_scheduler, 
        args=(TIME_INTERVAL_SECONDS_FOR_PRICES,),
        daemon=True
    )
    klines_thread = threading.Thread(
        target=run_klines_scheduler, 
        args=(TIME_INTERVAL_SECONDS_FOR_KLINES,),
        daemon=True
    )
    
    # Start both threads
    prices_thread.start()
    klines_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down schedulers...")