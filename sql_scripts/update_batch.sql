-- ==========================================
-- prices_binance quote_currency 업데이트
-- 100만 개씩 배치 처리
-- 여러 번 실행 가능 (안전)
-- ==========================================

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
    LIMIT 1000000
);

-- 업데이트 후 즉시 진행 상황 확인
SELECT 
    COUNT(*) as total,
    COUNT(quote_currency) as filled,
    COUNT(*) - COUNT(quote_currency) as remaining,
    ROUND(100.0 * COUNT(quote_currency) / COUNT(*), 2) as progress_pct
FROM schema_crypto.prices_binance;
