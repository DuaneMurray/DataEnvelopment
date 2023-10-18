SELECT Symbol, Date, `Net Income`, `Stockholders Equity`,

(`Net Income` / (`Total Assets` - `Total Liabilities Net Minority Interest`)) * 100 AS 'ROE',
(`EBIT` / (`Stockholders Equity`)) * 100 AS 'ROE2',
(`Net Income` / `Stockholders Equity`) * 100 AS 'ROE3',
((`Net Income` + (`Interest Expense`) * (1-`Tax Rate for Calcs`)) / `Total Assets`) * 100 AS 'ROA',
(`Net Income` / `Total Assets`)  * 100 AS 'ROA2',
(`EBIT` / `Invested Capital`)  * 100 AS 'ROC', 
(`EBIT` / `Total Revenue`) * 100 AS 'OpMargin',
(`Net Income` / `Total Revenue`) * 100  AS 'NetProfitMargin',
(`Net Income` / `Share Issued`) AS 'EPS',
(`Total Debt` / `Total Assets`)  * 100 AS 'DebtToAssets',
(`Total Debt` / (`Total Assets` - `Total Liabilities Net Minority Interest`)) * 100 AS 'DebtToEquity',
(`Total Liabilities Net Minority Interest` / `Stockholders Equity`) * 100 AS 'DebtToEquity2',
(`Total Non Current Liabilities Net Minority Interest` / `Stockholders Equity`) * 100 AS 'LTDebtToEquity',
(`Current Debt` / `Stockholders Equity`) * 100 AS 'STDebtToEquity',
(`Total Assets` - `Total Liabilities Net Minority Interest`) AS 'BookValue',
((`Total Assets` - `Total Liabilities Net Minority Interest`) / `Share Issued`) AS 'BVPS',
(`Current Assets` / `Current Liabilities`) AS 'CurrentRatio'
FROM stockdata.a_financials
WHERE symbol='AAPL';

#DELETE FROM stockdata.a_financials;