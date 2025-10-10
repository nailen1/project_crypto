-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema for quant data
CREATE SCHEMA IF NOT EXISTS quant;

-- Set default schema
SET search_path TO quant, public;

-- Create database_crypto schema
CREATE SCHEMA IF NOT EXISTS database_crypto;

-- Create binance_prices table
CREATE TABLE IF NOT EXISTS database_crypto.prices_binance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite unique constraint
    CONSTRAINT unique_symbol_datetime UNIQUE (symbol, datetime)
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_binance_prices_datetime ON database_crypto.prices_binance(datetime DESC);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol ON database_crypto.prices_binance(symbol);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol_datetime ON database_crypto.prices_binance(symbol, datetime DESC);

-- Create index for non-zero prices only (more efficient filtering)
CREATE INDEX IF NOT EXISTS idx_binance_prices_nonzero ON database_crypto.prices_binance(symbol, datetime DESC) 
WHERE price > 0;

COMMENT ON TABLE database_crypto.prices_binance IS 'Binance trading pair prices snapshot data';
COMMENT ON COLUMN database_crypto.prices_binance.datetime IS 'Snapshot timestamp from data source';
COMMENT ON COLUMN database_crypto.prices_binance.symbol IS 'Trading pair symbol (e.g., BTCUSDT, ETHBTC)';
COMMENT ON COLUMN database_crypto.prices_binance.price IS 'Price value (0 means inactive pair)';

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA quant TO juneyoung;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA quant TO juneyoung;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA quant TO juneyoung;

-- Grant permissions for database_crypto schema
GRANT ALL PRIVILEGES ON SCHEMA database_crypto TO juneyoung;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA database_crypto TO juneyoung;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA database_crypto TO juneyoung;

-- Log
DO $$
BEGIN
    RAISE NOTICE 'Quant database initialized successfully at %', NOW();
END $$;
