-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: stockdata
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company_beta_sigma`
--

DROP TABLE IF EXISTS `company_beta_sigma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_beta_sigma` (
  `index` bigint DEFAULT NULL,
  `Symbol` text,
  `Quarter` text,
  `Year` text,
  `MktIndex` text,
  `Beta` double DEFAULT NULL,
  `Sigma` double DEFAULT NULL,
  `StartDate` text,
  `EndDate` text,
  `StockReturnRate` double DEFAULT NULL,
  `MarketReturnRate` double DEFAULT NULL,
  `Period` text,
  `Sector` text,
  `StartPrice` double DEFAULT NULL,
  `EndPrice` double DEFAULT NULL,
  KEY `ix_company_beta_sigma_index` (`index`),
  KEY `ix_company_beta_sigma_symbol` (`Symbol`(15)),
  KEY `quarter_year` (`Quarter`(10),`Year`(5)),
  KEY `industry` (`Sector`(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `company_data_set`
--

DROP TABLE IF EXISTS `company_data_set`;
/*!50001 DROP VIEW IF EXISTS `company_data_set`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `company_data_set` AS SELECT 
 1 AS `symbol`,
 1 AS `exchangeShortName`,
 1 AS `sector`,
 1 AS `industry`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `company_details`
--

DROP TABLE IF EXISTS `company_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_details` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `price` double DEFAULT NULL,
  `beta` double DEFAULT NULL,
  `volAvg` bigint DEFAULT NULL,
  `mktCap` bigint DEFAULT NULL,
  `lastDiv` double DEFAULT NULL,
  `range` text,
  `changes` double DEFAULT NULL,
  `companyName` text,
  `currency` text,
  `cik` text,
  `isin` text,
  `cusip` text,
  `exchange` text,
  `exchangeShortName` text,
  `industry` text,
  `website` text,
  `description` text,
  `ceo` text,
  `sector` text,
  `country` text,
  `fullTimeEmployees` text,
  `phone` text,
  `address` text,
  `city` text,
  `state` text,
  `zip` text,
  `dcfDiff` text,
  `dcf` bigint DEFAULT NULL,
  `image` text,
  `ipoDate` text,
  `defaultImage` tinyint(1) DEFAULT NULL,
  `isEtf` tinyint(1) DEFAULT NULL,
  `isActivelyTrading` tinyint(1) DEFAULT NULL,
  `isAdr` tinyint(1) DEFAULT NULL,
  `isFund` tinyint(1) DEFAULT NULL,
  KEY `ix_company_details_index` (`index`),
  KEY `ix_company_details_symbol` (`symbol`(15))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_eps_pe`
--

DROP TABLE IF EXISTS `company_eps_pe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_eps_pe` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `date` text,
  `calendarYear` text,
  `period` text,
  `revenuePerShare` double DEFAULT NULL,
  `netIncomePerShare` double DEFAULT NULL,
  `operatingCashFlowPerShare` double DEFAULT NULL,
  `freeCashFlowPerShare` double DEFAULT NULL,
  `cashPerShare` double DEFAULT NULL,
  `bookValuePerShare` double DEFAULT NULL,
  `tangibleBookValuePerShare` double DEFAULT NULL,
  `shareholdersEquityPerShare` double DEFAULT NULL,
  `interestDebtPerShare` double DEFAULT NULL,
  `marketCap` double DEFAULT NULL,
  `enterpriseValue` double DEFAULT NULL,
  `peRatio` double DEFAULT NULL,
  `priceToSalesRatio` double DEFAULT NULL,
  `pocfratio` double DEFAULT NULL,
  `pfcfRatio` double DEFAULT NULL,
  `pbRatio` double DEFAULT NULL,
  `ptbRatio` double DEFAULT NULL,
  `evToSales` double DEFAULT NULL,
  `enterpriseValueOverEBITDA` double DEFAULT NULL,
  `evToOperatingCashFlow` double DEFAULT NULL,
  `evToFreeCashFlow` double DEFAULT NULL,
  `earningsYield` double DEFAULT NULL,
  `freeCashFlowYield` double DEFAULT NULL,
  `debtToEquity` double DEFAULT NULL,
  `debtToAssets` double DEFAULT NULL,
  `netDebtToEBITDA` double DEFAULT NULL,
  `currentRatio` double DEFAULT NULL,
  `interestCoverage` double DEFAULT NULL,
  `incomeQuality` double DEFAULT NULL,
  `dividendYield` double DEFAULT NULL,
  `payoutRatio` double DEFAULT NULL,
  `salesGeneralAndAdministrativeToRevenue` bigint DEFAULT NULL,
  `researchAndDdevelopementToRevenue` double DEFAULT NULL,
  `intangiblesToTotalAssets` double DEFAULT NULL,
  `capexToOperatingCashFlow` double DEFAULT NULL,
  `capexToRevenue` double DEFAULT NULL,
  `capexToDepreciation` double DEFAULT NULL,
  `stockBasedCompensationToRevenue` double DEFAULT NULL,
  `grahamNumber` double DEFAULT NULL,
  `roic` double DEFAULT NULL,
  `returnOnTangibleAssets` double DEFAULT NULL,
  `grahamNetNet` double DEFAULT NULL,
  `workingCapital` double DEFAULT NULL,
  `tangibleAssetValue` double DEFAULT NULL,
  `netCurrentAssetValue` double DEFAULT NULL,
  `investedCapital` double DEFAULT NULL,
  `averageReceivables` double DEFAULT NULL,
  `averagePayables` double DEFAULT NULL,
  `averageInventory` double DEFAULT NULL,
  `daysSalesOutstanding` double DEFAULT NULL,
  `daysPayablesOutstanding` double DEFAULT NULL,
  `daysOfInventoryOnHand` double DEFAULT NULL,
  `receivablesTurnover` double DEFAULT NULL,
  `payablesTurnover` double DEFAULT NULL,
  `inventoryTurnover` double DEFAULT NULL,
  `roe` double DEFAULT NULL,
  `capexPerShare` double DEFAULT NULL,
  KEY `ix_company_eps_pe_index` (`index`),
  KEY `ix_company_eps_pe_ix_symbol` (`symbol`(15)),
  KEY `year_and_period` (`calendarYear`(6),`period`(5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_ratios`
--

DROP TABLE IF EXISTS `company_ratios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_ratios` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `date` text,
  `calendarYear` text,
  `period` text,
  `currentRatio` double DEFAULT NULL,
  `quickRatio` double DEFAULT NULL,
  `cashRatio` double DEFAULT NULL,
  `daysOfSalesOutstanding` double DEFAULT NULL,
  `daysOfInventoryOutstanding` double DEFAULT NULL,
  `operatingCycle` double DEFAULT NULL,
  `daysOfPayablesOutstanding` double DEFAULT NULL,
  `cashConversionCycle` double DEFAULT NULL,
  `grossProfitMargin` double DEFAULT NULL,
  `operatingProfitMargin` double DEFAULT NULL,
  `pretaxProfitMargin` double DEFAULT NULL,
  `netProfitMargin` double DEFAULT NULL,
  `effectiveTaxRate` double DEFAULT NULL,
  `returnOnAssets` double DEFAULT NULL,
  `returnOnEquity` double DEFAULT NULL,
  `returnOnCapitalEmployed` double DEFAULT NULL,
  `netIncomePerEBT` double DEFAULT NULL,
  `ebtPerEbit` double DEFAULT NULL,
  `ebitPerRevenue` double DEFAULT NULL,
  `debtRatio` double DEFAULT NULL,
  `debtEquityRatio` double DEFAULT NULL,
  `longTermDebtToCapitalization` double DEFAULT NULL,
  `totalDebtToCapitalization` double DEFAULT NULL,
  `interestCoverage` double DEFAULT NULL,
  `cashFlowToDebtRatio` double DEFAULT NULL,
  `companyEquityMultiplier` double DEFAULT NULL,
  `receivablesTurnover` double DEFAULT NULL,
  `payablesTurnover` double DEFAULT NULL,
  `inventoryTurnover` double DEFAULT NULL,
  `fixedAssetTurnover` double DEFAULT NULL,
  `assetTurnover` double DEFAULT NULL,
  `operatingCashFlowPerShare` double DEFAULT NULL,
  `freeCashFlowPerShare` double DEFAULT NULL,
  `cashPerShare` double DEFAULT NULL,
  `payoutRatio` double DEFAULT NULL,
  `operatingCashFlowSalesRatio` double DEFAULT NULL,
  `freeCashFlowOperatingCashFlowRatio` double DEFAULT NULL,
  `cashFlowCoverageRatios` double DEFAULT NULL,
  `shortTermCoverageRatios` double DEFAULT NULL,
  `capitalExpenditureCoverageRatio` double DEFAULT NULL,
  `dividendPaidAndCapexCoverageRatio` double DEFAULT NULL,
  `dividendPayoutRatio` double DEFAULT NULL,
  `priceBookValueRatio` double DEFAULT NULL,
  `priceToBookRatio` double DEFAULT NULL,
  `priceToSalesRatio` double DEFAULT NULL,
  `priceEarningsRatio` double DEFAULT NULL,
  `priceToFreeCashFlowsRatio` double DEFAULT NULL,
  `priceToOperatingCashFlowsRatio` double DEFAULT NULL,
  `priceCashFlowRatio` double DEFAULT NULL,
  `priceEarningsToGrowthRatio` double DEFAULT NULL,
  `priceSalesRatio` double DEFAULT NULL,
  `dividendYield` double DEFAULT NULL,
  `enterpriseValueMultiple` double DEFAULT NULL,
  `priceFairValue` double DEFAULT NULL,
  KEY `ix_company_ratios_index` (`index`) /*!80000 INVISIBLE */,
  KEY `ix_company_ratios_symbol` (`symbol`(15)),
  KEY `year_and_period` (`calendarYear`(6),`period`(5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equity_prices`
--

DROP TABLE IF EXISTS `equity_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equity_prices` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `date` text,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `adjClose` double DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `unadjustedVolume` bigint DEFAULT NULL,
  `change` double DEFAULT NULL,
  `changePercent` double DEFAULT NULL,
  `vwap` double DEFAULT NULL,
  `label` text,
  `changeOverTime` double DEFAULT NULL,
  KEY `ix_equity_prices_index` (`index`),
  KEY `is_equity_prices_symbol` (`symbol`(15))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exchange_symbols`
--

DROP TABLE IF EXISTS `exchange_symbols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_symbols` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `name` text,
  `price` double DEFAULT NULL,
  `changesPercentage` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `dayLow` double DEFAULT NULL,
  `dayHigh` double DEFAULT NULL,
  `yearHigh` double DEFAULT NULL,
  `yearLow` double DEFAULT NULL,
  `marketCap` bigint DEFAULT NULL,
  `priceAvg50` double DEFAULT NULL,
  `priceAvg200` double DEFAULT NULL,
  `exchange` text,
  `volume` bigint DEFAULT NULL,
  `avgVolume` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `previousClose` double DEFAULT NULL,
  `eps` double DEFAULT NULL,
  `pe` double DEFAULT NULL,
  `earningsAnnouncement` text,
  `sharesOutstanding` bigint DEFAULT NULL,
  `timestamp` bigint DEFAULT NULL,
  KEY `ix_exchange_symbols_index` (`index`),
  KEY `is_exchange_symbols_symbol` (`symbol`(15))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `market_index`
--

DROP TABLE IF EXISTS `market_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `market_index` (
  `index` bigint DEFAULT NULL,
  `symbol` text,
  `date` text,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `adjClose` double DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `unadjustedVolume` bigint DEFAULT NULL,
  `change` double DEFAULT NULL,
  `changePercent` double DEFAULT NULL,
  `vwap` double DEFAULT NULL,
  `label` text,
  `changeOverTime` double DEFAULT NULL,
  KEY `ix_market_index_index` (`index`),
  KEY `ix_market_index_symbol` (`symbol`(15))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'stockdata'
--

--
-- Final view structure for view `company_data_set`
--

/*!50001 DROP VIEW IF EXISTS `company_data_set`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `company_data_set` AS select `company_details`.`symbol` AS `symbol`,`company_details`.`exchangeShortName` AS `exchangeShortName`,`company_details`.`sector` AS `sector`,`company_details`.`industry` AS `industry` from `company_details` where ((not((`company_details`.`symbol` like '%-%'))) and (`company_details`.`sector` is not null) and (`company_details`.`sector` <> '') and `company_details`.`symbol` in (select `company_ratios`.`symbol` from `company_ratios`)) order by `company_details`.`symbol` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-14 13:54:06
