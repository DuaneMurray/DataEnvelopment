#SELECT DISTINCT * FROM stockdata.exchange_symbols 
#WHERE exchange = 'NASDAQ' ORDER BY symbol ASC;

#SELECT COUNT(*) FROM stockdata.exchange_symbols

SELECT COUNT(*) FROM stockdata.exchange_symbols
WHERE exchange = 'NASDAQ';