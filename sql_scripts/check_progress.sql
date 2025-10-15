-- ==========================================
-- prices_binance 진행 상황 확인
-- ==========================================

SELECT 
    COUNT(*) as total_rows,
    COUNT(quote_currency) as filled_rows,
    COUNT(*) - COUNT(quote_currency) as remaining_rows,
    ROUND(100.0 * COUNT(quote_currency) / COUNT(*), 2) as progress_pct,
    TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS') as checked_at
FROM schema_crypto.prices_binance;