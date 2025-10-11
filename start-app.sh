#!/bin/bash

# Create necessary directories (상대 경로)
mkdir -p data/dataset-binance

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME}; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Start ETL in background
echo "Starting ETL process in background..."
python main.py &

# Start Jupyter in foreground (this keeps the container running)
echo "Starting Jupyter Notebook server..."
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""