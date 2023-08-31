SELECT DISTINCT p.symbol AS 'DMU',
b.beta AS 'Beta', b.sigma AS 'Sigma', f.debtToEquity AS 'DToE', 
f.pToBv AS 'PToB', f.netIncomeToRevenue AS 'NetMrgn', 
f.incomeNetPerWabso AS 'EPS', f.returnOnAssets AS 'ROA', 
f.returnOnEquity as 'ROE', b.rate_of_return as 'TTMreturn',
b.investment_entry_price AS 'entryPrice', b.one_year_price AS 'oneYRprice', b.three_year_price AS 'threeYRprice',
b.five_year_price AS 'fiveYRprice', Sector as 'Sector'
FROM price_quotes p, financials f, beta_sigma b, securities s
WHERE p.Symbol = b.Symbol AND p.Symbol = f.Symbol AND p.symbol = s.Symbol
AND p.date > '2014-12-31' AND p.date < '2016-01-01'
AND f.fiscalYear='2015'
AND b.one_year_price IS NOT NULL
AND b.three_year_price IS NOT NULL
AND b.five_year_price IS NOT NULL
AND f.returnOnEquity IS NOT NULL
AND f.debtToEquity != 0
AND s.Sector = 'Basic Materials';