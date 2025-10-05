-- Create binance_prices table
CREATE TABLE IF NOT EXISTS quant.binance_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite unique constraint
    CONSTRAINT unique_symbol_datetime UNIQUE (symbol, datetime)
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_binance_prices_datetime ON quant.binance_prices(datetime DESC);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol ON quant.binance_prices(symbol);
CREATE INDEX IF NOT EXISTS idx_binance_prices_symbol_datetime ON quant.binance_prices(symbol, datetime DESC);

-- Create index for non-zero prices only (more efficient filtering)
CREATE INDEX IF NOT EXISTS idx_binance_prices_nonzero ON quant.binance_prices(symbol, datetime DESC) 
WHERE price > 0;

COMMENT ON TABLE quant.binance_prices IS 'Binance trading pair prices snapshot data';
COMMENT ON COLUMN quant.binance_prices.datetime IS 'Snapshot timestamp from data source';
COMMENT ON COLUMN quant.binance_prices.symbol IS 'Trading pair symbol (e.g., BTCUSDT, ETHBTC)';
COMMENT ON COLUMN quant.binance_prices.price IS 'Price value (0 means inactive pair)';