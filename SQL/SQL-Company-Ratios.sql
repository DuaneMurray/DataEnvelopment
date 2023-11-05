#SELECT * FROM stockdata.company_ratios
#WHERE symbol = '';

#SELECT COUNT(*) FROM stockdata.company_ratios;

##################################################
# NO MATCHING COMPANY DETAIL & COMPANY RATIO ROWS
##################################################
#SELECT 
#    company_details.symbol,
#    company_details.ipoDate,
#    isActivelyTrading
#FROM
#    company_details
#WHERE
#    LENGTH(company_details.symbol) < 5
#        AND company_details.exchangeShortName = 'NASDAQ'
#        AND company_details.symbol NOT IN (SELECT 
#            company_ratios.symbol
#        FROM
#            company_ratios)

#################################################
# MATCHING COMPANY DETAIL & COMPANY RATIO ROWS
#################################################
SELECT 
    company_details.symbol, company_details.exchangeShortName, 
    company_details.sector, company_details.industry
FROM
    company_details
WHERE
    symbol NOT LIKE "%-%"
	/*
    #AND LENGTH(company_details.symbol) < 5
	#AND company_details.exchangeShortName = 'AMEX'
	#AND sector = 'Technology'
    */
    AND sector IS NOT NULL
    AND sector != ''
    AND company_details.symbol IN (
		SELECT company_ratios.symbol
        FROM company_ratios
        )
	order by symbol ASC
