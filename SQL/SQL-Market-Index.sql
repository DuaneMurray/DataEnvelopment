#SELECT * FROM stockdata.market_index;

# GET THE SP500 DATA
#SELECT * FROM stockdata.market_index
#WHERE symbol = '^GSPC';

# GET THE DOW JONES INDUSTRICAL DATA
#SELECT * FROM stockdata.market_index
#WHERE symbol = '^DJI';

# GET THE NASDAQ INDEX DATA
#SELECT * FROM stockdata.market_index
#WHERE symbol = '^IXIC';

SELECT symbol, date, close, 
(((open - close)/ close)) AS 'pct_change'
FROM market_index
WHERE symbol= '^GSPC'
#AND date = DATE_SUB('2015-12-31', INTERVAL 30 DAY) 
AND (date BETWEEN DATE_SUB('2016-12-31', INTERVAL 1 MONTH) AND '2016-12-31')