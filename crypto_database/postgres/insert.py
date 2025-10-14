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

def insert_binance_prices(data: List[Dict], table_name: str = 'schema_crypto.prices_binance'):
    """
    Insert list of Binance prices into database
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
    

def insert_binance_klines(data: List[Dict], table_name: str = 'schema_crypto.klines_binance'):
    """
    Insert list of Binance klines into database
    """
    from .connector import get_engine
    
    engine = get_engine()
    
    inserted_count = 0
    skipped_count = 0
    failed_count = 0
    
    with engine.connect() as conn:
        for kline in data:
            # 필수 필드 검증
            symbol = kline.get('symbol')
            datetime_open = kline.get('datetime_open')
            datetime_close = kline.get('datetime_close')
            
            if not symbol or not datetime_open or not datetime_close:
                logger.warning(f"Missing required fields in kline: {kline}")
                failed_count += 1
                continue
            
            # datetime 타입 변환 처리
            if isinstance(datetime_open, str):
                try:
                    datetime_open = datetime.strptime(datetime_open, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    logger.error(f"Invalid datetime_open format '{datetime_open}': {e}")
                    failed_count += 1
                    continue
            
            if isinstance(datetime_close, str):
                try:
                    datetime_close = datetime.strptime(datetime_close, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    logger.error(f"Invalid datetime_close format '{datetime_close}': {e}")
                    failed_count += 1
                    continue
            
            try:
                # Decimal 변환
                params = {
                    'symbol': symbol,
                    'datetime_open': datetime_open,
                    'datetime_close': datetime_close,
                    'open': Decimal(str(kline.get('open'))) if kline.get('open') is not None else None,
                    'high': Decimal(str(kline.get('high'))) if kline.get('high') is not None else None,
                    'low': Decimal(str(kline.get('low'))) if kline.get('low') is not None else None,
                    'close': Decimal(str(kline.get('close'))) if kline.get('close') is not None else None,
                    'volume': Decimal(str(kline.get('volume'))) if kline.get('volume') is not None else None,
                    'quote_volume': Decimal(str(kline.get('quote_volume'))) if kline.get('quote_volume') is not None else None,
                    'trades_count': int(kline.get('trades_count')) if kline.get('trades_count') is not None else None,
                    'taker_buy_volume': Decimal(str(kline.get('taker_buy_volume'))) if kline.get('taker_buy_volume') is not None else None,
                    'taker_buy_quote_volume': Decimal(str(kline.get('taker_buy_quote_volume'))) if kline.get('taker_buy_quote_volume') is not None else None
                }
                
                result = conn.execute(
                    text(f"""
                        INSERT INTO {table_name} (
                            symbol, datetime_open, datetime_close,
                            open, high, low, close,
                            volume, quote_volume, trades_count,
                            taker_buy_volume, taker_buy_quote_volume
                        )
                        VALUES (
                            :symbol, :datetime_open, :datetime_close,
                            :open, :high, :low, :close,
                            :volume, :quote_volume, :trades_count,
                            :taker_buy_volume, :taker_buy_quote_volume
                        )
                        ON CONFLICT (symbol, datetime_open) 
                        DO NOTHING
                    """),
                    params
                )
                
                if result.rowcount > 0:
                    inserted_count += 1
                else:
                    skipped_count += 1
                
            except Exception as e:
                logger.error(f"Failed to insert {symbol} at {datetime_open}: {type(e).__name__}: {e}")
                failed_count += 1
                continue
        
        conn.commit()
    
    result = {
        'total_klines': len(data),
        'inserted': inserted_count,
        'skipped': skipped_count,
        'failed': failed_count
    }
    
    if failed_count > 0:
        logger.warning(f"Insert result: {result}")
    else:
        logger.info(f"Insert result: {result}")
    
    return result