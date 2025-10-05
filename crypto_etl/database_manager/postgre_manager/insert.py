"""
Insert Binance data (list of dictionaries) into database
"""
from sqlalchemy import text
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Union


def insert_binance_data(data: List[Dict], table_name: str = 'quant.binance_prices'):
    """
    Insert list of Binance price snapshots into database
    """
    from .connector import get_engine
    
    engine = get_engine()
    
    inserted_count = 0
    skipped_count = 0
    failed_count = 0
    
    with engine.connect() as conn:
        for snapshot in data:
            dt = snapshot.get('datetime')
            if not dt:
                failed_count += 1
                continue
            
            if isinstance(dt, str):
                try:
                    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    failed_count += 1
                    continue
            
            for symbol, price in snapshot.items():
                if symbol == 'datetime':
                    continue
                
                if price is None:
                    continue
                
                try:
                    price_decimal = Decimal(str(price))
                    
                    result = conn.execute(
                        text(f"""
                            INSERT INTO {table_name} (datetime, symbol, price)
                            VALUES (:datetime, :symbol, :price)
                            ON CONFLICT (symbol, datetime) 
                            DO NOTHING
                        """),
                        {
                            'datetime': dt,
                            'symbol': symbol,
                            'price': price_decimal
                        }
                    )
                    
                    # rowcount로 실제 INSERT 여부 확인
                    if result.rowcount > 0:
                        inserted_count += 1
                    else:
                        skipped_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    continue
        
        conn.commit()
    
    return {
        'total_snapshots': len(data),
        'inserted': inserted_count,      # 실제 INSERT된 개수
        'skipped': skipped_count,        # 중복으로 스킵된 개수
        'failed': failed_count
    }