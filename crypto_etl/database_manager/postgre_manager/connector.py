from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database credentials
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME')
encoded_password = quote_plus(db_password)
database_url = f"postgresql+psycopg://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"


def get_engine():
    engine = create_engine(
    database_url,
    echo=False,
    pool_pre_ping=True
    )
    return engine

def test_connection():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database(), current_user;"))
        db, user = result.fetchone()
        print(f"Connected to database: {db}")
        print(f"Connected as user: {user}")

if __name__ == "__main__":
    test_connection()