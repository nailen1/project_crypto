# Crypto ETL

A cryptocurrency data extraction, transformation, and loading (ETL) system for collecting market data from Binance.

## Features

- **Real-time Data Collection**: Automatically collects cryptocurrency market data from Binance API
- **Scheduled Execution**: Runs data collection at regular intervals (every 10 seconds)
- **CSV Export**: Saves collected data to CSV files with timestamps
- **Error Handling**: Robust error handling and recovery mechanisms
- **Easy Setup**: Simple installation and configuration process

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd module-crypto_etl
```

2. Create environment configuration file:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual values
# Required variables:
# - DB_USER: Database username (replace 'your_name' with your actual username)
# - DB_PASSWORD: Database password (use strong password)
# - DB_NAME: Database name (e.g., database_crypto)
# - PGADMIN_EMAIL: pgAdmin login email
# - PGADMIN_PASSWORD: pgAdmin login password
```

3. Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

4. Activate the virtual environment:

```bash
source .env-crypto/bin/activate
```

## Usage

### Running with Docker

```bash
# Build and start the container
docker compose up -d

# Check container status
docker compose ps

# View logs
docker compose logs -f
```

### Running the Data Collection Scheduler

```bash
python main.py
```

This will start the continuous data collection process. Press `Ctrl+C` to stop.

### Project Structure

```
module-crypto_etl/
├── crypto_etl/           # Main package
│   └── extractors/       # Data extractors
│       └── binance/      # Binance-specific extractor
├── data/                 # Data storage directory
│   └── dataset-binance/  # Collected CSV files
├── main.py              # Main entry point
├── setup.sh             # Setup script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration

The system collects data every 10 seconds by default. You can modify the interval by editing the `TIME_INTERVAL_SECONDS` variable in `main.py`.

## Data Output

Collected data is saved as CSV files in the `data/dataset-binance/` directory with the following naming convention:

```
dataset-binance_api-at{timestamp}.csv
```

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue in the repository.
