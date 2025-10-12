# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (PostgreSQL client only)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter
# RUN pip install --no-cache-dir jupyter notebook jupyterlab

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Jupyter port
# EXPOSE 8888

# Copy and setup startup script
COPY start-app.sh /app/start-app.sh
RUN chmod +x /app/start-app.sh

# Default command
CMD ["/app/start-app.sh"]