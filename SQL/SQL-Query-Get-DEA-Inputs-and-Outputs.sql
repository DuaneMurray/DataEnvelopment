SELECT 
	b.symbol AS 'DMU', 
	#b.Year,
    #b.Quarter,
    #monthname(b.StartDate) AS 'Month',
	b.beta AS 'Beta', 
	b.sigma AS 'Sigma', 
	r.debtEquityRatio AS 'DToE', 
	r.priceToBookRatio AS 'PToB', 
	r.netProfitMargin AS 'NetMrgn',
    e.netIncomePerShare as 'EPS',
	r.returnOnAssets AS 'ROA', 
	r.returnOnEquity as 'ROE',
	b.StockReturnRate as 'TrailingReturn',
    p.Close AS 'entryPrice',
    p.Close AS 'oneYRprice',
    p.Close AS 'threeYRprice',
    p.Close AS 'fiveYRprice',
    b.Sector AS 'Sector'
FROM 
	stockdata.company_beta_sigma b, 
	stockdata.company_ratios r,
    stockdata.company_eps_pe e,
    stockdata.equity_prices p
WHERE 
	b.Sector = 'Utilities'
    AND monthname(b.StartDate) = 'January'
    
	AND b.Year = '2020'
	AND b.Quarter = 'Q1'
	AND r.calendarYear = '2020'
	AND r.Period = 'Q1'
    AND e.calendarYear = '2020'
    AND e.period = 'Q1'
    
	AND b.Symbol = r.Symbol
	AND p.Symbol = b.Symbol
    AND e.Symbol = b.Symbol
	
    AND b.beta != 0
	AND b.sigma != 0 
	AND r.debtEquityRatio != 0
	AND r.priceToBookRatio != 0
	AND r.netProfitMargin != 0
	AND e.netIncomePerShare != 0
	AND r.returnOnAssets != 0 
	AND r.returnOnEquity != 0
	AND b.StockReturnRate != 0
	AND p.Close != 0
    
    AND p.date = b.EndDate