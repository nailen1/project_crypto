
QUERY_PRICES_XUSDT_WITHIN_6HRS = """
SELECT datetime, symbol, price 
FROM schema_crypto.prices_binance
WHERE symbol LIKE '%USDT'
  AND datetime >= NOW() - INTERVAL '6 hours'
ORDER BY datetime ASC;
"""

QUERY_PRICE_BTCUSDT = """
SELECT datetime, symbol, price 
FROM schema_crypto.prices_binance
WHERE symbol = 'BTCUSDT'
ORDER BY datetime ASC;
"""

QUERY_PRICES_TEMPLATE = """
SELECT datetime, symbol, price 
FROM schema_crypto.prices_binance
WHERE symbol LIKE '%USDT'
  AND datetime >= NOW() - INTERVAL '{interval}'
ORDER BY datetime ASC;
"""

# query_6h = QUERY_PRICES_TEMPLATE.format('6 hours')
# query_12h = QUERY_PRICES_TEMPLATE.format('12 hours')
# query_1d = QUERY_PRICES_TEMPLATE.format('1 day')


QUERY_PRICE_SYMBOL_TEMPLATE = """
SELECT datetime, symbol, price 
FROM schema_crypto.prices_binance
WHERE symbol = '{symbol}'
ORDER BY datetime ASC;
"""

# query_price_symbol = QUERY_PRICE_SYMBOL_TEMPLATE.format(symbol='BTCUSDT')