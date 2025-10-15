-- ==========================================
-- PostgreSQL 프로세스 상태 확인
-- ==========================================

-- 활성 쿼리 및 트랜잭션 확인
SELECT 
    pid,
    state,
    NOW() - query_start as duration,
    NOW() - xact_start as transaction_duration,
    LEFT(query, 100) as query_preview
FROM pg_stat_activity 
WHERE datname = 'database_crypto'
  AND pid != pg_backend_pid()
ORDER BY xact_start;