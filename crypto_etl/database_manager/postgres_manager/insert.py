"""
Insert Binance data (list of dictionaries) into database
"""
from sqlalchemy import text
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Union
import logging

# 로거 설정
logger = logging.getLogger(__name__)

def insert_binance_data(data: List[Dict], table_name: str = 'schema_crypto.prices_binance'):
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
                logger.warning(f"Missing datetime in snapshot: {snapshot}")  # ← 추가
                failed_count += 1
                continue
            
            if isinstance(dt, str):
                try:
                    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    logger.error(f"Invalid datetime format '{dt}': {e}")  # ← 추가
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
                    
                    if result.rowcount > 0:
                        inserted_count += 1
                    else:
                        skipped_count += 1
                    
                except Exception as e:
                    # ← 핵심 개선: 에러 내용을 로그에 출력!
                    logger.error(f"Failed to insert {symbol} at {dt}: {type(e).__name__}: {e}")
                    failed_count += 1
                    continue
        
        conn.commit()
    
    result = {
        'total_snapshots': len(data),
        'inserted': inserted_count,
        'skipped': skipped_count,
        'failed': failed_count
    }
    
    # ← 추가: 결과 요약 로그
    if failed_count > 0:
        logger.warning(f"Insert result: {result}")
    else:
        logger.info(f"Insert result: {result}")
    
    return result