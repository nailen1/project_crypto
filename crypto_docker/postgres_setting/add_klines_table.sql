-- Add klines_binance table to existing database
-- This script is idempotent (can be run multiple times safely)

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

-- Add comments
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

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'klines_binance table created successfully at %', NOW();
END $$;