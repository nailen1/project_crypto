-- ==========================================
-- 002: Add quote_currency (BATCH)
-- Safe batch processing (1M rows at a time)
-- ==========================================

-- prices_binance 배치 업데이트
DO $$
DECLARE
    batch_size INTEGER := 1000000;
    updated_count INTEGER := 0;
    total_updated INTEGER := 0;
BEGIN
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'Starting batch update for prices_binance';
    RAISE NOTICE '===========================================';
    
    LOOP
        UPDATE schema_crypto.prices_binance
        SET quote_currency = 
            CASE 
                WHEN symbol LIKE '%USDT' THEN 'USDT'
                WHEN symbol LIKE '%BUSD' THEN 'BUSD'
                WHEN symbol LIKE '%USDC' THEN 'USDC'
                WHEN symbol LIKE '%TUSD' THEN 'TUSD'
                WHEN symbol LIKE '%BTC' THEN 'BTC'
                WHEN symbol LIKE '%ETH' THEN 'ETH'
                WHEN symbol LIKE '%BNB' THEN 'BNB'
                WHEN symbol LIKE '%TRX' THEN 'TRX'
                WHEN symbol LIKE '%XRP' THEN 'XRP'
                ELSE 'OTHER'
            END
        WHERE id IN (
            SELECT id 
            FROM schema_crypto.prices_binance 
            WHERE quote_currency IS NULL 
            LIMIT batch_size
        );
        
        GET DIAGNOSTICS updated_count = ROW_COUNT;
        total_updated := total_updated + updated_count;
        
        RAISE NOTICE 'Batch completed: % rows (total: %)', updated_count, total_updated;
        
        -- 더 이상 업데이트할 행이 없으면 종료
        EXIT WHEN updated_count = 0;
        
        -- 1초 대기 (서버 부하 감소)
        PERFORM pg_sleep(1);
    END LOOP;
    
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'prices_binance completed!';
    RAISE NOTICE 'Total updated: % rows', total_updated;
    RAISE NOTICE '===========================================';
END $$;

-- klines_binance 배치 업데이트
DO $$
DECLARE
    batch_size INTEGER := 1000000;
    updated_count INTEGER := 0;
    total_updated INTEGER := 0;
BEGIN
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'Starting batch update for klines_binance';
    RAISE NOTICE '===========================================';
    
    LOOP
        UPDATE schema_crypto.klines_binance
        SET quote_currency = 
            CASE 
                WHEN symbol LIKE '%USDT' THEN 'USDT'
                WHEN symbol LIKE '%BUSD' THEN 'BUSD'
                WHEN symbol LIKE '%USDC' THEN 'USDC'
                WHEN symbol LIKE '%TUSD' THEN 'TUSD'
                WHEN symbol LIKE '%BTC' THEN 'BTC'
                WHEN symbol LIKE '%ETH' THEN 'ETH'
                WHEN symbol LIKE '%BNB' THEN 'BNB'
                ELSE 'OTHER'
            END
        WHERE id IN (
            SELECT id 
            FROM schema_crypto.klines_binance 
            WHERE quote_currency IS NULL 
            LIMIT batch_size
        );
        
        GET DIAGNOSTICS updated_count = ROW_COUNT;
        total_updated := total_updated + updated_count;
        
        RAISE NOTICE 'Batch completed: % rows (total: %)', updated_count, total_updated;
        
        EXIT WHEN updated_count = 0;
        
        PERFORM pg_sleep(1);
    END LOOP;
    
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'klines_binance completed!';
    RAISE NOTICE 'Total updated: % rows', total_updated;
    RAISE NOTICE '===========================================';
END $$;

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_prices_quote_datetime 
ON schema_crypto.prices_binance(quote_currency, datetime DESC);

CREATE INDEX IF NOT EXISTS idx_klines_quote_datetime 
ON schema_crypto.klines_binance(quote_currency, datetime_open DESC);

-- 최종 통계
DO $$
DECLARE
    prices_total INTEGER;
    prices_usdt INTEGER;
    klines_total INTEGER;
    klines_usdt INTEGER;
BEGIN
    SELECT COUNT(*) INTO prices_total FROM schema_crypto.prices_binance;
    SELECT COUNT(*) INTO prices_usdt FROM schema_crypto.prices_binance WHERE quote_currency = 'USDT';
    SELECT COUNT(*) INTO klines_total FROM schema_crypto.klines_binance;
    SELECT COUNT(*) INTO klines_usdt FROM schema_crypto.klines_binance WHERE quote_currency = 'USDT';
    
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'ALL COMPLETED!';
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'prices_binance: % total, % USDT', prices_total, prices_usdt;
    RAISE NOTICE 'klines_binance: % total, % USDT', klines_total, klines_usdt;
    RAISE NOTICE '===========================================';
END $$;
