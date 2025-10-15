-- ==========================================
-- 현재 실행 중인 쿼리 확인
-- ==========================================

SELECT 
    pid,
    state,
    NOW() - query_start as duration,
    LEFT(query, 80) as query_preview
FROM pg_stat_activity 
WHERE datname = 'database_crypto'
  AND pid != pg_backend_pid()
  AND state != 'idle'
ORDER BY query_start;
