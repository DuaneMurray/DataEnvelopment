#SELECT COUNT(*) FROM stockdata.company_details
#WHERE sector = '';

#SELECT DISTINCT exchangeShortName FROM stockdata.company_details;

#SELECT COUNT(*) FROM company_details
#WHERE exchangeShortName = 'NASDAQ';

#SELECT DISTINCT sector FROM company_details
#WHERE sector IS NOT NULL AND sector != ''
#ORDER BY sector ASC;

#SELECT count(DISTINCT industry) FROM company_details
#WHERE industry IS NOT NULL AND industry != ''
#ORDER BY industry ASC;

#SELECT COUNT(*) FROM company_details
#WHERE sector = 'Communication Services';

#SELECT COUNT(*) FROM company_details
#WHERE industry = 'Airlines';