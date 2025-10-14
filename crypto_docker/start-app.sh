#!/bin/bash

# Create data directory
mkdir -p data/dataset-binance

# Wait for PostgreSQL
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME}; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run ETL in foreground
echo "Starting ETL process..."
exec python main.py