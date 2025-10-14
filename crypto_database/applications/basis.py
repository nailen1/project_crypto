import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import text
from crypto_database.postgres.connector import get_engine


def get_df_by_query(query: str, engine=None) -> pd.DataFrame:
    """
    Execute a query and return results as a pandas DataFrame.
    
    Args:
        query: SQL query string
        engine: SQLAlchemy engine (if None, creates a new one)
    """
    if engine is None:
        engine = get_engine()
    
    df = pd.read_sql(text(query), engine)
    return df
