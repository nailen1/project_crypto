-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema for quant data
CREATE SCHEMA IF NOT EXISTS quant;

-- Set default schema
SET search_path TO quant, public;

-- Create schema_crypto schema
CREATE SCHEMA IF NOT EXISTS schema_crypto;

-- Create binance_prices table
CREATE TABLE IF NOT EXISTS schema_crypto.prices_binance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite unique constraint
    CONSTRAINT unique_symbol_datetime UNIQUE (symbol, datetime)
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_binance_prices_datetime ON schema_crypto.prices_binance(datetime DESC);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol ON schema_crypto.prices_binance(symbol);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol_datetime ON schema_crypto.prices_binance(symbol, datetime DESC);

-- Create index for non-zero prices only (more efficient filtering)
CREATE INDEX IF NOT EXISTS idx_binance_prices_nonzero ON schema_crypto.prices_binance(symbol, datetime DESC) 
WHERE price > 0;

COMMENT ON TABLE schema_crypto.prices_binance IS 'Binance trading pair prices snapshot data';
COMMENT ON COLUMN schema_crypto.prices_binance.datetime IS 'Snapshot timestamp from data source';
COMMENT ON COLUMN schema_crypto.prices_binance.symbol IS 'Trading pair symbol (e.g., BTCUSDT, ETHBTC)';
COMMENT ON COLUMN schema_crypto.prices_binance.price IS 'Price value (0 means inactive pair)';

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA quant TO :DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA quant TO :DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA quant TO :DB_USER;

-- Grant permissions for schema_crypto schema
GRANT ALL PRIVILEGES ON SCHEMA schema_crypto TO :DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA schema_crypto TO :DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA schema_crypto TO :DB_USER;

-- Log
DO $$
BEGIN
    RAISE NOTICE 'Quant database initialized successfully at %', NOW();
END $$;
