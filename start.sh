#!/bin/bash

# Start PostgreSQL
echo "Starting PostgreSQL..."
service postgresql start

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h localhost -p 5432 -U ${DB_USER}; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Initialize database schema and permissions
echo "Initializing database schema..."
PGPASSWORD=${DB_PASSWORD} psql -h localhost -p 5432 -U ${DB_USER} -d ${DB_NAME} -v DB_USER=${DB_USER} -f /app/init.sql
echo "Database initialization completed!"

# Start PgAdmin in background
echo "Starting PgAdmin..."
pgadmin4 --port=5050 --host=0.0.0.0 &

# Start ETL in background
echo "Starting ETL process in background..."
python main.py &

# Start Jupyter in foreground (this keeps the container running)
echo "Starting Jupyter Notebook server..."
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""
