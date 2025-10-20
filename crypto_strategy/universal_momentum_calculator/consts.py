
import os
from pathlib import Path

# Get the project root directory (parent of crypto_etl)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / 'data'

FILE_FOLDER_BINANCE = str(DATA_ROOT / 'dataset-binance')
FILE_FOLDER_CACHE = str(DATA_ROOT / 'data-cache')
