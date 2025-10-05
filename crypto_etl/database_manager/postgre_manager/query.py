"""
Query data by datetime snapshots
"""
from sqlalchemy import text
from typing import Optional

def query_by_datetime_snapshots(
    n_snapshots: int = 1,
    table_name: str = 'quant.binance_prices',
    option_include_created_at: bool = False,
    option_exclude_zero: bool = True
):
    """
    Query all data from latest N datetime snapshots
    
    Args:
        n_snapshots: Number of latest datetime snapshots to retrieve
        table_name: Table name
        option_include_created_at: Include created_at column
        option_exclude_zero: Exclude price = 0 records
    
    Returns:
        List of dictionaries
        
    Example:
        # Latest snapshot only
        data = query_by_datetime_snapshots(n_snapshots=1)
        
        # Latest 3 snapshots
        data = query_by_datetime_snapshots(n_snapshots=3)
        
        # All snapshots with zero prices
        data = query_by_datetime_snapshots(n_snapshots=10, option_exclude_zero=False)
    """
    from .connector import get_engine
    
    engine = get_engine()
    
    # Select columns
    if option_include_created_at:
        columns = "symbol, price, datetime, created_at"
    else:
        columns = "symbol, price, datetime"
    
    # Build WHERE clause
    where_clause = "WHERE price > 0" if option_exclude_zero else ""
    
    query = f"""
        WITH latest_datetimes AS (
            SELECT DISTINCT datetime
            FROM {table_name}
            ORDER BY datetime DESC
            LIMIT :n_snapshots
        )
        SELECT {columns}
        FROM {table_name}
        WHERE datetime IN (SELECT datetime FROM latest_datetimes)
        {("AND price > 0" if option_exclude_zero else "")}
        ORDER BY datetime DESC, symbol;
    """
    
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {'n_snapshots': n_snapshots}
        )
        rows = result.fetchall()
        
        # Convert to list of dicts
        data = []
        for row in rows:
            item = {
                'symbol': row.symbol,
                'price': float(row.price),
                'datetime': row.datetime
            }
            if option_include_created_at:
                item['created_at'] = row.created_at
            data.append(item)
        
        return data