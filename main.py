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

from crypto_etl.extractors.binance.scheduler import run_scheduler

TIME_INTERVAL_SECONDS = 10

if __name__ == "__main__":
    run_scheduler(time_interval_seconds=TIME_INTERVAL_SECONDS)
