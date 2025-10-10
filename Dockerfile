# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Build arguments
ARG DB_USER=crypto_user
ARG DB_PASSWORD=crypto_password
ARG DB_NAME=crypto_db

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter
RUN pip install --no-cache-dir jupyter notebook jupyterlab

# Install PgAdmin
RUN pip install --no-cache-dir pgadmin4

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/dataset-binance

# Setup PostgreSQL
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" && \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};" && \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

# Expose ports
EXPOSE 8888 5432 80

# Copy and setup startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]
