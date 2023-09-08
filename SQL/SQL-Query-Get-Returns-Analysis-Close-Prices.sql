SELECT date, close FROM stock.price_quotes 
WHERE symbol = 'CDZI' 
AND 
(
date = '2020-12-31' 
OR date = '2019-12-31'
OR date = '2018-12-31'
OR date = '2017-12-29'
OR date = '2016-01-04' /* INVESTMENT DATE */
OR date = '2016-12-30'
OR date = '2015-12-30'
)
order by date DESC;