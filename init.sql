-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema for quant data
CREATE SCHEMA IF NOT EXISTS quant;

-- Set default schema
SET search_path TO quant, public;

-- Create exchange_rates table
CREATE TABLE IF NOT EXISTS quant.exchange_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(20, 8) NOT NULL,
    volume_24h NUMERIC(20, 8),
    market_cap NUMERIC(20, 2),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_symbol_timestamp UNIQUE (symbol, timestamp)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_exchange_rates_symbol ON quant.exchange_rates(symbol);
CREATE INDEX IF NOT EXISTS idx_exchange_rates_timestamp ON quant.exchange_rates(timestamp DESC);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA quant TO juneyoung;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA quant TO juneyoung;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA quant TO juneyoung;

-- Log
DO $$
BEGIN
    RAISE NOTICE 'Quant database initialized successfully at %', NOW();
END $$;
