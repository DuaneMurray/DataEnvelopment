# STANDARD DEVIATION (Sigma) OF PRICES OVER TIME RANGE
#
#SELECT STDDEV(close) AS Sigma
#FROM equity_prices
#WHERE symbol = 'AAPL'
#AND (date BETWEEN '2015-01-02' AND '2015-12-31')

# SLOPE CALCULATION - START DATE VALUE
#
#SELECT close AS start_close
#FROM equity_prices
#WHERE symbol = 'AAPL'
#AND date = '2015-01-02'

# SLOPE CALCULATION - END DATE VALUE
#SELECT close AS end_close
#FROM equity_prices
#WHERE symbol = 'AAPL'
#AND date = '2015-12-31'

# PCT CHANGE IN CLOSE PRICES = (start_close - end_close) / end_close

# DO THE SAME PROCESS FOR S&P 500 INDEX VALUES FOR PCT CHANGE

# CALCULATE THE BETA: stock pct change / market pct change

SELECT date, close 
FROM equity_prices
#WHERE date = DATE_SUB('2015-12-31', INTERVAL 30 DAY) 
WHERE date = DATE_SUB('2015-12-31', INTERVAL 1 MONTH)
AND symbol = 'AAPL';
