import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()


def get_engine():
    """
    Create and return a SQLAlchemy engine.
    작동하는 코드와 완전히 동일한 방식으로 구현
    """
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(database_url)
    return engine


def test_connection(
    db_user: Optional[str] = None,
    db_password: Optional[str] = None,
    db_host: Optional[str] = None,
    db_port: Optional[str] = None,
    db_name: Optional[str] = None
):
    """
    Test database connection and print connection details.
    
    Args:
        db_user: Database username (defaults to DB_USER env var)
        db_password: Database password (defaults to DB_PASSWORD env var)
        db_host: Database host (defaults to DB_HOST env var or 'localhost')
        db_port: Database port (defaults to DB_PORT env var or '5432')
        db_name: Database name (defaults to DB_NAME env var)
    """
    try:
        engine = get_engine(db_user, db_password, db_host, db_port, db_name)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user;"))
            db, user = result.fetchone()
            print(f"✅ Connected to database: {db}")
            print(f"✅ Connected as user: {user}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()