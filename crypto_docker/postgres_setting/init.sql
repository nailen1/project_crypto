-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema_crypto schema
CREATE SCHEMA IF NOT EXISTS schema_crypto;

-- Set default schema
SET search_path TO schema_crypto, public;

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

-- Create binance_klines table
CREATE TABLE IF NOT EXISTS schema_crypto.klines_binance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) NOT NULL,
    datetime_open TIMESTAMP WITH TIME ZONE NOT NULL,
    datetime_close TIMESTAMP WITH TIME ZONE NOT NULL,
    open NUMERIC(20, 8),
    high NUMERIC(20, 8),
    low NUMERIC(20, 8),
    close NUMERIC(20, 8),
    volume NUMERIC(30, 8),
    quote_volume NUMERIC(30, 8),
    trades_count INTEGER,
    taker_buy_volume NUMERIC(30, 8),
    taker_buy_quote_volume NUMERIC(30, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite unique constraint
    CONSTRAINT unique_symbol_datetime_open UNIQUE (symbol, datetime_open)
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_binance_klines_datetime_open ON schema_crypto.klines_binance(datetime_open DESC);
CREATE INDEX IF NOT EXISTS idx_binance_klines_datetime_close ON schema_crypto.klines_binance(datetime_close DESC);
CREATE INDEX IF NOT EXISTS idx_binance_klines_symbol ON schema_crypto.klines_binance(symbol);
CREATE INDEX IF NOT EXISTS idx_binance_klines_symbol_datetime ON schema_crypto.klines_binance(symbol, datetime_open DESC);

-- Create index for active trading pairs (non-zero volume)
CREATE INDEX IF NOT EXISTS idx_binance_klines_active ON schema_crypto.klines_binance(symbol, datetime_open DESC) 
WHERE volume > 0;

COMMENT ON TABLE schema_crypto.klines_binance IS 'Binance klines (candlestick) OHLCV data';
COMMENT ON COLUMN schema_crypto.klines_binance.symbol IS 'Trading pair symbol (e.g., BTCUSDT, ETHBTC)';
COMMENT ON COLUMN schema_crypto.klines_binance.datetime_open IS 'Kline open time';
COMMENT ON COLUMN schema_crypto.klines_binance.datetime_close IS 'Kline close time';
COMMENT ON COLUMN schema_crypto.klines_binance.open IS 'Open price';
COMMENT ON COLUMN schema_crypto.klines_binance.high IS 'High price';
COMMENT ON COLUMN schema_crypto.klines_binance.low IS 'Low price';
COMMENT ON COLUMN schema_crypto.klines_binance.close IS 'Close price';
COMMENT ON COLUMN schema_crypto.klines_binance.volume IS 'Trading volume in base asset';
COMMENT ON COLUMN schema_crypto.klines_binance.quote_volume IS 'Trading volume in quote asset';
COMMENT ON COLUMN schema_crypto.klines_binance.trades_count IS 'Number of trades';
COMMENT ON COLUMN schema_crypto.klines_binance.taker_buy_volume IS 'Taker buy volume in base asset';
COMMENT ON COLUMN schema_crypto.klines_binance.taker_buy_quote_volume IS 'Taker buy volume in quote asset';

-- Log
DO $$
BEGIN
    RAISE NOTICE 'Crypto database initialized successfully at %', NOW();
END $$;