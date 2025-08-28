SELECT T1.`Percent (%) Eligible Free (K-12)` FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.County = 'Alameda' ORDER BY T1.`Percent (%) Eligible Free (K-12)` DESC LIMIT 1
SELECT (CAST(`Free Meal Count (Ages 5-17)` AS REAL) / `Enrollment (Ages 5-17)`) AS `Percent (%) Eligible Free (Ages 5-17)` FROM frpm WHERE `Educational Option Type` = 'Continuation School' ORDER BY `Percent (%) Eligible Free (Ages 5-17)` ASC LIMIT 3
SELECT T2.Zip FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 AND T1.`District Name` = 'Fresno County Office of Education'
SELECT T2.MailStreet FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode ORDER BY T1.`FRPM Count (K-12)` DESC LIMIT 1
SELECT T2.Phone FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 AND T2.OpenDate > '2000-01-01'
SELECT COUNT(*) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F' AND T1.AvgScrMath > 400
SELECT T1.School FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T2.NumTstTakr > 500 AND T1.Magnet = 1
SELECT T2.Phone FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.NumGE1500 > 0 ORDER BY T1.NumGE1500 DESC LIMIT 1
SELECT T1.NumTstTakr FROM satscores AS T1 INNER JOIN frpm AS T2 ON T1.cds = T2.CDSCode ORDER BY T2.`FRPM Count (K-12)` DESC LIMIT 1
SELECT COUNT(*) FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.AvgScrMath > 560 AND T2.FundingType = 'Directly funded'
SELECT T1.`FRPM Count (Ages 5-17)` FROM frpm AS T1 JOIN satscores AS T2 ON T1.CDSCode = T2.cds ORDER BY T2.AvgScrRead DESC LIMIT 1
SELECT CDSCode FROM frpm WHERE `Enrollment (K-12)` + `Enrollment (Ages 5-17)` > 500
SELECT T2.`Percent (%) Eligible Free (Ages 5-17)` FROM satscores AS T1 INNER JOIN frpm AS T2 ON T1.cds = T2.CDSCode WHERE CAST(T1.NumGE1500 AS REAL) / T1.NumTstTakr > 0.3 ORDER BY T2.`Percent (%) Eligible Free (Ages 5-17)` DESC LIMIT 1
SELECT T2.Phone FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY CAST(T1.NumGE1500 AS REAL) / T1.NumTstTakr DESC LIMIT 3
SELECT schools.NCESSchool FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode ORDER BY `Enrollment (Ages 5-17)` DESC LIMIT 5
SELECT T2.District FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.StatusType = 'Active' GROUP BY T2.District ORDER BY AVG(T1.AvgScrRead) DESC LIMIT 1
SELECT COUNT(CASE WHEN T1.StatusType = 'Merged' AND T2.NumTstTakr < 100 THEN T1.CDSCode END) FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
SELECT S1.CharterNum FROM schools AS S1 JOIN satscores AS S2 ON S1.CDSCode = S2.cds WHERE S2.AvgScrWrite > 499 AND S1.CharterNum IS NOT NULL ORDER BY S2.AvgScrWrite DESC
SELECT COUNT(T1.CDSCode) FROM frpm AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds INNER JOIN schools AS T3 ON T1.CDSCode = T3.CDSCode WHERE T1.`County Name` = 'Fresno' AND T3.FundingType = 'Directly funded' AND T2.NumTstTakr < 250
SELECT T2.Phone FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrMath DESC LIMIT 1
SELECT COUNT(CDSCode) FROM frpm WHERE `County Name` = 'Amador' AND `Low Grade` = '9' AND `High Grade` = '12'
SELECT COUNT(*) FROM frpm WHERE `County Name` = 'Los Angeles' AND `Free Meal Count (K-12)` > 500 AND `Free Meal Count (K-12)` < 700
SELECT sname FROM satscores WHERE cname = 'Contra Costa' ORDER BY NumTstTakr DESC LIMIT 1
SELECT T2.School, T2.Street FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE (T1.`Enrollment (K-12)` - T1.`Enrollment (Ages 5-17)`) > 30
SELECT T1.`School Name` FROM frpm AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.`Percent (%) Eligible Free (K-12)` > 0.1 AND T2.NumGE1500 >= 1
SELECT T2.School, T2.FundingType FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.County = 'Riverside' AND T1.AvgScrMath > 400
SELECT T2.School, T2.Street, T2.City, T2.State, T2.Zip FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`School Type` = 'High Schools (Public)' AND T1.`County Name` = 'Monterey' AND T1.`FRPM Count (Ages 5-17)` > 800
SELECT T1.AvgScrWrite, T2.School, T2.Phone FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE (STRFTIME('%Y', T2.OpenDate) < '1992' OR STRFTIME('%Y', T2.ClosedDate) < '2000')
SELECT s.School, s.DOCType FROM frpm AS frp JOIN schools AS s ON frp.CDSCode = s.CDSCode WHERE (frp.`Enrollment (K-12)` - frp.`Enrollment (Ages 5-17)`) > (SELECT AVG(enrollment_difference) FROM (SELECT (frp.`Enrollment (K-12)` - frp.`Enrollment (Ages 5-17)`) AS enrollment_difference FROM frpm AS frp JOIN schools AS s ON frp.CDSCode = s.CDSCode WHERE s.FundingType = 'Locally funded')) AND s.FundingType = 'Locally funded'
SELECT T1.OpenDate FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.`School Type` = 'K-12 Schools (Public)' ORDER BY T2.`Enrollment (K-12)` DESC LIMIT 1
SELECT T2.City FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Enrollment (K-12)` IS NOT NULL ORDER BY T1.`Enrollment (K-12)` ASC LIMIT 5
SELECT CAST(`Free Meal Count (K-12)` AS REAL) / `Enrollment (K-12)` FROM frpm ORDER BY `Enrollment (K-12)` DESC LIMIT 11
SELECT T1.`FRPM Count (K-12)` / T1.`Enrollment (K-12)` AS FRPM_Rate FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.SOC = 66 ORDER BY T1.`FRPM Count (K-12)` DESC LIMIT 5
SELECT T2.Website, T2.School FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Free Meal Count (Ages 5-17)` BETWEEN 1900 AND 2000
SELECT CAST(T1.`Free Meal Count (Ages 5-17)` AS REAL) / T1.`Enrollment (Ages 5-17)` AS FreeRate FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.`AdmFName1` = 'Kacey' AND T2.`AdmLName1` = 'Gibson'
SELECT T2.AdmEmail1 FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 ORDER BY T1.`Enrollment (K-12)` ASC LIMIT 1
SELECT T2.AdmFName1, T2.AdmLName1, T2.AdmFName2, T2.AdmLName2, T2.AdmFName3, T2.AdmLName3 FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.NumGE1500 >= 1500 ORDER BY T1.NumGE1500 DESC LIMIT 1
SELECT T2.Street, T2.City, T2.State, T2.Zip FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY CAST(T1.NumGE1500 AS REAL) / T1.NumTstTakr ASC LIMIT 1
SELECT T1.Website FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.County = 'Los Angeles' AND T2.NumTstTakr BETWEEN 2000 AND 3000
SELECT AVG(T1.NumTstTakr) FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.County = 'Fresno' AND T2.OpenDate BETWEEN '1980-01-01' AND '1980-12-31'
SELECT T1.Phone FROM schools AS T1 JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.District = 'Fresno Unified' ORDER BY T2.AvgScrRead ASC LIMIT 1
SELECT T1.School FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.Virtual = 'F' ORDER BY T2.AvgScrRead DESC LIMIT 5
SELECT T2.EdOpsName FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrMath DESC LIMIT 1
SELECT T2.AvgScrMath, T2.cname FROM (SELECT cds, AvgScrMath + AvgScrRead + AvgScrWrite AS total_score FROM satscores ORDER BY total_score ASC LIMIT 1) AS T1 INNER JOIN satscores AS T2 ON T1.cds = T2.cds
SELECT T1.AvgScrWrite, T2.City FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.NumGE1500 DESC LIMIT 1
SELECT T1.School, T2.AvgScrWrite FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.AdmFName1 = 'Ricci' AND T1.AdmLName1 = 'Ulrich'
SELECT T1.School FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.DOC = 31 AND T1.GSserved = 'K-12' ORDER BY T2.`Enrollment (K-12)` DESC LIMIT 1
SELECT CAST(COUNT(CDSCode) AS REAL) / 12 FROM schools WHERE County = 'Alameda' AND DOC = 52 AND STRFTIME('%Y', OpenDate) = '1980'
SELECT CAST(SUM(CASE WHEN DOC = 54 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN DOC = 52 THEN 1 ELSE 0 END) FROM schools WHERE County = 'Orange' AND StatusType = 'Merged'
SELECT County, School, ClosedDate FROM schools WHERE StatusType = 'Closed' GROUP BY County ORDER BY COUNT(ClosedDate) DESC LIMIT 1
SELECT T2.Street, T2.School FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrMath DESC LIMIT 1 OFFSET 6
SELECT T2.MailStreet, T2.School FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrRead ASC LIMIT 1
SELECT COUNT(T1.cds) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.NumGE1500 > 0 AND T2.MailCity = 'Lakeport'
SELECT SUM(T2.NumTstTakr) FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.MailCity = 'Fresno'
SELECT T1.School, T1.MailZip FROM schools AS T1 JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.AdmFName1 = 'Avetik' AND T1.AdmLName1 = 'Atoian'
SELECT CAST(SUM(CASE WHEN s.County = 'Colusa' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN s.County = 'Humboldt' THEN 1 ELSE 0 END) AS ratio FROM schools s WHERE s.MailState = 'CA'
SELECT COUNT(CDSCode) FROM schools WHERE MailState = 'CA' AND MailCity = 'San Joaquin' AND StatusType = 'Active'
SELECT T2.Phone, T2.Ext  FROM satscores AS T1  JOIN schools AS T2  ON T1.cds = T2.CDSCode  ORDER BY T1.AvgScrWrite DESC  LIMIT 1 OFFSET 332
SELECT Phone, Ext, School FROM schools WHERE Zip = '95203-3704'
SELECT T1.Website FROM schools AS T1 WHERE (T1.AdmFName1 = 'Mike' AND T1.AdmLName1 = 'Larson') OR (T1.AdmFName1 = 'Dante' AND T1.AdmLName1 = 'Alvarez')
SELECT Website FROM schools WHERE Virtual = 'P' AND Charter = 1 AND County = 'San Joaquin'
SELECT COUNT(*) FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.Charter = 1 AND T1.City = 'Hickman' AND T1.DOC = 52
SELECT COUNT(*) FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.Charter = 0 AND T2.County = 'Los Angeles' AND (T1.`Free Meal Count (K-12)` * 100) / T1.`Enrollment (K-12)` < 0.18
SELECT AdmFName1, AdmLName1, AdmFName2, AdmLName2, AdmFName3, AdmLName3, School, City FROM schools WHERE Charter = 1 AND CharterNum = '00D2'
SELECT COUNT(CDSCode) FROM schools WHERE MailCity = 'Hickman' AND CharterNum = '00D4'
SELECT (CAST(COUNT(CASE WHEN FundingType = 'Locally funded' THEN 1 ELSE NULL END) AS REAL) * 100) / COUNT(*) FROM schools WHERE County = 'Santa Clara'
SELECT COUNT(*) FROM schools WHERE County = 'Stanislaus' AND FundingType = 'Directly funded' AND OpenDate BETWEEN '2000-01-01' AND '2005-12-31'
SELECT COUNT(CDSCode) FROM schools WHERE StatusType = 'Closed' AND DOCType = 'Community College District' AND City = 'San Francisco' AND STRFTIME('%Y', ClosedDate) = '1989'
SELECT T1.County FROM schools AS T1 WHERE T1.ClosedDate BETWEEN '1980-01-01' AND '1989-12-31' AND T1.SOC = 11 GROUP BY T1.County ORDER BY COUNT(*) DESC LIMIT 1
SELECT NCESDist FROM schools WHERE SOC = 31
SELECT COUNT(CDSCode) FROM schools WHERE County = 'Alpine' AND StatusType IN ('Closed', 'Active') AND SOCType = 'District Community Day Schools'
SELECT District FROM schools WHERE City = 'Fresno' AND Magnet = 0
SELECT T1.`Enrollment (Ages 5-17)` FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.County = 'Alameda' AND T2.City = 'Fremont' AND T2.DocType = 'State Special Schools'
SELECT T1.`FRPM Count (Ages 5-17)` FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.`EdOpsName` = 'Youth Authority School' AND T2.`MailStreet` = 'PO Box 1040'
SELECT T2.`Low Grade` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.NCESDist = '0613360' AND T1.EdOpsName = 'District Special Education Consortia School' ORDER BY T2.`Low Grade` ASC LIMIT 1
SELECT T1.EILName, T2.`School Name`  FROM schools AS T1  INNER JOIN frpm AS T2  ON T1.CDSCode = T2.CDSCode  WHERE T2.`County Code` = '37'    AND T2.`NSLP Provision Status` = 'Breakfast Provision 2'
SELECT T2.City FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`NSLP Provision Status` = 'Lunch Provision 2' AND T1.`Low Grade` = '9' AND T1.`High Grade` = '12' AND T2.County = 'Merced' AND T2.EILCode = 'HS'
SELECT T1.`School Name`, (CAST(T1.`FRPM Count (Ages 5-17)` AS REAL) / T1.`Enrollment (Ages 5-17)`) * 100 AS Percent_Eligible_FRPM FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.County = 'Los Angeles' AND T2.GSserved = 'K-9'
SELECT GSserved FROM schools WHERE City = 'Adelanto' GROUP BY GSserved ORDER BY COUNT(GSserved) DESC LIMIT 1
SELECT County, COUNT(CDSCode) AS NumberOfSchools FROM schools WHERE Virtual = 'F' AND County IN ('San Diego', 'Santa Barbara') GROUP BY County ORDER BY NumberOfSchools DESC LIMIT 1
SELECT T1.`School Type`, T1.`School Name`, T2.Latitude FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode ORDER BY T2.Latitude DESC LIMIT 1
SELECT T1.City, T2.`Low Grade`, T1.`School` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.State = 'CA' ORDER BY T1.Latitude ASC LIMIT 1
SELECT GSoffered FROM schools ORDER BY Longitude DESC LIMIT 1
SELECT  T1.City, COUNT(T1.CDSCode) AS NumberOfSchools FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.Magnet = 1 AND T1.GSoffered = 'K-8' AND T2.`NSLP Provision Status` = 'Multiple Provision Types' GROUP BY T1.City
SELECT T1.AdmFName1, T1.District FROM schools AS T1 GROUP BY T1.AdmFName1, T1.District ORDER BY COUNT(T1.AdmFName1) DESC LIMIT 2
SELECT T1.`Percent (%) Eligible Free (K-12)`, T2.District FROM frpm AS T1 JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.AdmFName1 = 'Alusine'
SELECT AdmLName1, District, County, School FROM schools WHERE CharterNum = '0040'
SELECT DISTINCT AdmEmail1, AdmEmail2, AdmEmail3 FROM schools WHERE County = 'San Bernardino' AND District = 'San Bernardino City Unified' AND (SOC = 62 OR DOC = 54) AND OpenDate BETWEEN '2009-01-01' AND '2010-12-31'
SELECT T2.AdmEmail1, T1.Sname FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.NumGE1500 > 0 ORDER BY T1.NumGE1500 DESC LIMIT 1
SELECT COUNT(*) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.frequency = 'POPLATEK PO OBRATU' AND T2.A3 = 'east Bohemia'
SELECT COUNT(T1.account_id) FROM account AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A3 = 'Prague'
SELECT AVG(A12) AS avg_1995, AVG(A13) AS avg_1996,         CASE WHEN AVG(A12) > AVG(A13) THEN '1995' ELSE '1996' END AS higher_rate_year  FROM district
SELECT COUNT(district_id) FROM district WHERE A11 > 6000 AND A11 < 10000
SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'M' AND T2.A3 = 'north Bohemia' AND T2.A11 > 8000
SELECT T1.account_id, (SELECT MAX(A11) FROM district) - (SELECT MIN(A11) FROM district) AS salary_gap FROM account AS T1 JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.gender = 'F' ORDER BY T2.birth_date ASC LIMIT 1
SELECT T3.account_id FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id JOIN disp AS T3 ON T1.client_id = T3.client_id ORDER BY (CURRENT_DATE - T1.birth_date), T2.A11 DESC LIMIT 1
SELECT COUNT(T3.client_id) FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.frequency = 'POPLATEK TYDNE' AND T2.type = 'OWNER'
SELECT T3.client_id FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.frequency = 'POPLATEK PO OBRATU' AND T2.type = 'DISPONENT'
SELECT T2.account_id FROM loan AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id WHERE STRFTIME('%Y', T1.`date`) = '1997' AND T2.frequency = 'POPLATEK TYDNE' ORDER BY T1.amount ASC LIMIT 1
SELECT T1.account_id FROM account AS T1 JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T2.duration > 12 AND STRFTIME('%Y', T1.date) = '1993' ORDER BY T2.amount DESC LIMIT 1
SELECT COUNT(*) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Sokolov' AND T1.gender = 'F' AND strftime('%Y', T1.birth_date) < '1950'
SELECT account_id FROM trans WHERE `date` LIKE '1995%' ORDER BY `date` ASC LIMIT 1
SELECT DISTINCT T2.account_id FROM account AS T2 INNER JOIN trans AS T1 ON T2.account_id = T1.account_id WHERE T2.date < '1997-01-01' AND T1.amount > 3000
SELECT T1.client_id FROM client AS T1 JOIN card AS T2 ON T1.client_id = T2.disp_id WHERE T2.issued = '1994-03-03'
SELECT T2.date FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.date = '1998-10-14' AND T1.amount = 840
SELECT T3.district_id FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.`date` = '1994-08-25'
SELECT MAX(T3.amount) FROM client AS T1  INNER JOIN card AS T2 ON T1.client_id = T2.disp_id  INNER JOIN trans AS T3 ON T2.card_id = T3.account_id  WHERE T2.issued = '1996-10-21'
SELECT T1.gender FROM client AS T1 INNER JOIN account AS T2 ON T1.district_id = T2.district_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id ORDER BY T1.birth_date ASC LIMIT 1
SELECT T4.amount FROM client AS T1 JOIN disp AS T2 ON T1.client_id = T2.client_id JOIN loan AS T3 ON T2.account_id = T3.account_id JOIN trans AS T4 ON T3.account_id = T4.account_id WHERE T3.amount = (SELECT MAX(amount) FROM loan) ORDER BY T4.date ASC LIMIT 1
SELECT COUNT(T1.client_id) FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id JOIN disp AS T3 ON T1.client_id = T3.client_id JOIN account AS T4 ON T3.account_id = T4.account_id WHERE T2.A2 = 'Jesenik' AND T1.gender = 'F'
SELECT T3.disp_id FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN disp AS T3 ON T2.account_id = T3.account_id INNER JOIN client AS T4 ON T3.client_id = T4.client_id WHERE T1.amount = 5100 AND T1.date = '1998-09-02'
SELECT COUNT(*) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Litomerice' AND STRFTIME('%Y', T1.date) = '1996'
SELECT T3.A2 FROM client AS T1 JOIN disp AS T2 ON T1.client_id = T2.client_id JOIN account AS T4 ON T2.account_id = T4.account_id JOIN district AS T3 ON T4.district_id = T3.district_id WHERE T1.gender = 'F' AND T1.birth_date = '1976-01-29'
SELECT T3.birth_date FROM loan AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.`date` = '1996-01-03' AND T1.amount = 98832
SELECT T2.account_id FROM client AS T1 JOIN account AS T2 ON T1.district_id = T2.district_id JOIN district AS T3 ON T1.district_id = T3.district_id WHERE T3.A3 = 'Prague' ORDER BY T2.date LIMIT 1
SELECT CAST(SUM(CASE WHEN T1.gender = 'M' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.client_id)  FROM client AS T1  JOIN district AS T2  ON T1.district_id = T2.district_id  WHERE T2.A3 = 'south Bohemia'  ORDER BY T2.A4 DESC  LIMIT 1
SELECT ( ( SELECT balance FROM trans WHERE date = '1993-03-22' ) - ( SELECT balance FROM trans WHERE date = '1998-12-27' ) ) / ( SELECT balance FROM trans WHERE date = '1998-12-27' ) * 100 AS increase_rate FROM account JOIN disp ON account.account_id = disp.account_id JOIN loan ON disp.account_id = loan.account_id WHERE loan.`date` = ( SELECT MIN(`date`) FROM loan WHERE `date` LIKE '1993-07-05' )
SELECT (SUM(CASE WHEN status = 'A' THEN amount ELSE 0 END) * 100.0) / SUM(amount) AS percentage_paid FROM loan
SELECT CAST(COUNT(CASE WHEN amount < 100000 AND status = 'C' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM loan
SELECT T1.account_id, T2.A2, T2.A3 FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE STRFTIME('%Y', T1.`date`) = '1993' AND T1.frequency = 'POPLATEK PO OBRATU'
SELECT T1.account_id, T1.frequency FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T2.client_id = T3.client_id JOIN district AS T4 ON T3.district_id = T4.district_id WHERE T4.A3 = 'east Bohemia' AND T1.date BETWEEN '1995-01-01' AND '2000-12-31'
SELECT T1.account_id, T1.date FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Prachatice'
SELECT T3.A2, T3.A3 FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.loan_id = 4990
SELECT DISTINCT T2.account_id, T4.A2, T4.A3 FROM loan AS T2 JOIN account AS T3 ON T2.account_id = T3.account_id JOIN district AS T4 ON T3.district_id = T4.district_id WHERE T2.amount > 300000
SELECT T1.loan_id, T3.A3, T3.A11 FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.duration = 60
SELECT T4.A2, T4.A3, (CAST(T4.A13 - T4.A12 AS REAL) * 100) / T4.A12 AS unemployment_rate_increment FROM district AS T4 INNER JOIN client AS T2 ON T4.district_id = T2.district_id INNER JOIN disp AS T3 ON T2.client_id = T3.client_id INNER JOIN account AS T1 ON T3.account_id = T1.account_id INNER JOIN loan AS T5 ON T1.account_id = T5.account_id WHERE T5.status = 'D'
SELECT CAST(COUNT(CASE WHEN T2.A2 = 'Decin' THEN T1.account_id ELSE NULL END) AS REAL) * 100 / COUNT(T1.account_id) FROM account AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id WHERE STRFTIME('%Y', T1.date) = '1993'
SELECT account_id FROM account WHERE frequency = 'POPLATEK MESICNE'
SELECT T1.A2, COUNT(T2.client_id) AS num_female_account_holders FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.gender = 'F' GROUP BY T1.A2 ORDER BY num_female_account_holders DESC LIMIT 9
SELECT T3.A2 AS district_name, SUM(T1.amount) AS total_withdrawal FROM trans AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.type = 'VYDAJ' AND T1.date LIKE '1996-01%' GROUP BY T3.A2 ORDER BY total_withdrawal DESC LIMIT 10
SELECT COUNT(*) FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id LEFT JOIN card AS T3 ON T1.client_id = T3.disp_id WHERE T2.A3 = 'south Bohemia' AND T3.card_id IS NULL
SELECT T1.A3 FROM district AS T1 JOIN account AS T2 ON T1.district_id = T2.district_id JOIN loan AS T3 ON T2.account_id = T3.account_id WHERE T3.status = 'C' GROUP BY T1.A3 ORDER BY COUNT(T3.loan_id) DESC LIMIT 1
SELECT AVG(T3.amount) FROM account AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id INNER JOIN loan AS T3 ON T1.account_id = T3.account_id INNER JOIN client AS T4 ON T2.client_id = T4.client_id WHERE T4.gender = 'M'
SELECT district_id, A2 FROM district ORDER BY A13 DESC LIMIT 1
SELECT COUNT(T2.account_id) FROM district AS T1 JOIN account AS T2 ON T1.district_id = T2.district_id ORDER BY A16 DESC LIMIT 1
SELECT COUNT(*) AS negative_balance_accounts  FROM trans AS T1  JOIN disp AS T2 ON T1.account_id = T2.account_id  JOIN account AS T3 ON T1.account_id = T3.account_id  WHERE T1.operation = 'VYBER KARTOU'    AND T3.frequency = 'POPLATEK MESICNE'    AND T1.balance < 0
SELECT COUNT(*) FROM account AS T1 JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T1.frequency = 'POPLATEK MESICNE' AND T2.status = 'A' AND T2.amount >= 250000 AND T2.`date` BETWEEN '1995-01-01' AND '1997-12-31'
SELECT COUNT(*) FROM account AS T1 JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T1.district_id = 1 AND T2.status IN ('C', 'D')
SELECT COUNT(T2.client_id) FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.gender = 'M' AND T1.district_id IN (SELECT district_id FROM district ORDER BY A15 DESC LIMIT 1 OFFSET 1)
SELECT COUNT(*) FROM card AS T1 INNER JOIN disp AS T2 ON T1.disp_id = T2.disp_id WHERE T1.type = 'gold' AND T2.type = 'OWNER'
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Pisek'
SELECT DISTINCT T3.A2 FROM trans AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id JOIN district AS T3 ON T2.district_id = T3.district_id WHERE STRFTIME('%Y', T1.date) = '1997' AND T1.amount > 10000
SELECT T2.account_id FROM district AS T1 JOIN account AS T3 ON T1.district_id = T3.district_id JOIN `order` AS T2 ON T2.account_id = T3.account_id WHERE T2.k_symbol = 'SIPO' AND T1.A2 = 'Pisek'
SELECT T2.account_id FROM card AS T1 INNER JOIN disp AS T3 ON T1.disp_id = T3.disp_id INNER JOIN account AS T2 ON T3.account_id = T2.account_id WHERE T1.type = 'gold'
SELECT AVG(T1.amount) FROM trans AS T1 INNER JOIN card AS T2 ON T1.account_id = T2.card_id WHERE T1.type = 'VYBER KARTOU' AND STRFTIME('%Y', T1.date) = '2021'
SELECT T2.account_id FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.`date` LIKE '1998%' AND T1.operation = 'VYBER KARTOU' AND T1.amount < ( SELECT AVG(amount) FROM trans WHERE `date` LIKE '1998%' AND operation = 'VYBER KARTOU' )
SELECT T1.client_id FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN account AS T3 ON T2.account_id = T3.account_id INNER JOIN card AS T4 ON T2.disp_id = T4.disp_id INNER JOIN loan AS T5 ON T3.account_id = T5.account_id WHERE T1.gender = 'F' AND T2.type = 'OWNER'
SELECT COUNT(T1.client_id) FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'F' AND T2.A3 = 'south Bohemia'
SELECT DISTINCT T1.account_id FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.district_id = (SELECT district_id FROM district WHERE A2 = 'Tabor') AND T2.type = 'OWNER'
SELECT DISTINCT T2.type FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id JOIN client AS T3 ON T1.district_id = T3.district_id JOIN district AS T4 ON T1.district_id = T4.district_id WHERE T2.type <> 'OWNER' AND T4.A11 BETWEEN 8000 AND 9000
SELECT COUNT(account.account_id) FROM account INNER JOIN district ON account.district_id = district.district_id INNER JOIN trans ON account.account_id = trans.account_id WHERE district.A3 = 'north Bohemia' AND trans.bank = 'AB'
SELECT DISTINCT T3.A2 FROM trans AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.type = 'VYDAJ'
SELECT AVG(T1.A15) FROM district AS T1 INNER JOIN account AS T2 ON T1.district_id = T2.district_id WHERE T1.A4 > 4000 AND T2.date >= '1997-01-01' AND T2.date < '1998-01-01'
SELECT COUNT(*) FROM card AS t1 JOIN disp AS t2 ON t1.disp_id = t2.disp_id WHERE t1.type = 'classic' AND t2.type = 'OWNER'
SELECT COUNT(*) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Hl.m. Praha' AND T1.gender = 'M'
SELECT CAST(COUNT(CASE WHEN type = 'gold' AND STRFTIME('%Y', issued) < '1998' THEN card_id END) AS REAL) * 100 / COUNT(card_id) FROM card
SELECT T3.client_id FROM account AS T1 JOIN loan AS T2 ON T1.account_id = T2.account_id JOIN disp AS T4 ON T1.account_id = T4.account_id JOIN client AS T3 ON T4.client_id = T3.client_id ORDER BY T2.amount DESC LIMIT 1
SELECT T1.A15 FROM district AS T1 INNER JOIN account AS T2 ON T1.district_id = T2.district_id WHERE T2.account_id = 532
SELECT T2.district_id FROM `order` AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.order_id = 33333
SELECT operation FROM trans WHERE account_id IN (SELECT account_id FROM disp WHERE client_id = 3356) AND operation = 'VYBER'
SELECT COUNT(account.account_id) FROM account INNER JOIN loan ON account.account_id = loan.account_id WHERE account.frequency = 'POPLATEK TYDNE' AND loan.amount < 200000
SELECT T3.type FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN card AS T3 ON T2.disp_id = T3.disp_id WHERE T1.client_id = 13539
SELECT T2.A3 FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.client_id = 3541
SELECT T3.A2 FROM loan AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.status = 'A' GROUP BY T2.district_id ORDER BY COUNT(T2.account_id) DESC LIMIT 1
SELECT T1.client_id FROM client AS T1 JOIN disp AS T2 ON T1.client_id = T2.client_id JOIN account AS T3 ON T2.account_id = T3.account_id WHERE T2.account_id IN (SELECT account_id FROM `order` WHERE order_id = 32423)
SELECT T2.* FROM account AS T1 JOIN trans AS T2 ON T1.account_id = T2.account_id WHERE T1.district_id = 5
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Jesenik'
SELECT client.client_id FROM client JOIN disp ON client.client_id = disp.client_id JOIN card ON disp.disp_id = card.disp_id WHERE card.type = 'junior' AND card.issued > '1996-12-31'
SELECT CAST(COUNT(CASE WHEN T1.gender = 'F' THEN 1 END) AS REAL) * 100 / COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A11 > 10000
SELECT (CAST(SUM(CASE WHEN STRFTIME('%Y', T1.`date`) = '1997' THEN T1.amount ELSE 0 END) - SUM(CASE WHEN STRFTIME('%Y', T1.`date`) = '1996' THEN T1.amount ELSE 0 END) AS REAL) * 100) / SUM(CASE WHEN STRFTIME('%Y', T1.`date`) = '1996' THEN T1.amount ELSE 0 END) FROM loan AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id INNER JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T3.gender = 'M'
SELECT COUNT(*) FROM trans WHERE operation = 'VYBER KARTOU' AND `date` > '1995-12-31'
SELECT (SUM(CASE WHEN A3 = 'north Bohemia' THEN A16 ELSE 0 END) - SUM(CASE WHEN A3 = 'east Bohemia' THEN A16 ELSE 0 END)) AS crime_difference FROM district
SELECT COUNT(disp_id) FROM disp WHERE account_id BETWEEN 1 AND 10 AND type IN ('OWNER', 'DISPONENT')
SELECT T2.k_symbol FROM account AS T1 INNER JOIN trans AS T2 ON T1.account_id = T2.account_id WHERE T1.account_id = 3 AND T2.amount = 3539
SELECT STRFTIME('%Y', T1.birth_date) FROM client AS T1 JOIN disp AS T2 ON T1.client_id = T2.client_id WHERE T2.disp_id = 130
SELECT COUNT(T1.account_id) FROM account AS T1 JOIN disp AS T2 ON T1.account_id = T2.account_id WHERE T2.type = 'OWNER' AND T1.frequency = 'POPLATEK PO OBRATU'
SELECT T1.amount, T1.status FROM loan AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id WHERE T2.client_id = 992
SELECT T1.amount, T4.gender FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN disp AS T3 ON T2.account_id = T3.account_id INNER JOIN client AS T4 ON T3.client_id = T4.client_id WHERE T1.trans_id = 852 AND T2.district_id IN (SELECT district_id FROM client WHERE client_id = 4) AND T4.client_id = 4
SELECT T2.type FROM client AS T1 INNER JOIN card AS T2 ON T1.client_id = T2.disp_id WHERE T1.client_id = 9
SELECT SUM(trans.amount) AS total_paid FROM trans INNER JOIN account ON trans.account_id = account.account_id INNER JOIN disp ON account.account_id = disp.account_id INNER JOIN client ON disp.client_id = client.client_id WHERE client.client_id = 617 AND STRFTIME('%Y', trans.date) = '1998'
SELECT DISTINCT C1.client_id FROM client AS C1 INNER JOIN account AS A1 ON C1.district_id = A1.district_id INNER JOIN district AS D1 ON A1.district_id = D1.district_id WHERE C1.birth_date BETWEEN '1983-01-01' AND '1987-12-31' AND D1.A3 = 'east Bohemia'
SELECT T1.client_id FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN loan AS T3 ON T2.account_id = T3.account_id WHERE T1.gender = 'F' ORDER BY T3.amount DESC LIMIT 3
SELECT COUNT(*) FROM client AS T1 JOIN trans AS T2 ON T1.client_id = T2.account_id WHERE T1.gender = 'M' AND STRFTIME('%Y', T1.birth_date) BETWEEN '1974' AND '1976' AND T2.amount > 4000 AND T2.k_symbol = 'SIPO'
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Beroun' AND T1.date > '1996-12-31'
SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN card AS T2 ON T1.client_id = T2.disp_id WHERE T1.gender = 'F' AND T2.type = 'junior'
SELECT CAST(COUNT(CASE WHEN T1.gender = 'F' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM client AS T1 JOIN account AS T2 ON T1.district_id = T2.district_id WHERE T2.district_id IN (SELECT district_id FROM district WHERE A3 = 'Prague')
SELECT CAST(SUM(CASE WHEN T2.gender = 'M' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T2.client_id) AS percentage_male_clients FROM account AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T1.frequency = 'POPLATEK TYDNE'
SELECT COUNT(T3.client_id) FROM account AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id INNER JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.frequency = 'POPLATEK TYDNE' AND T2.type = 'OWNER'
SELECT T1.account_id FROM account AS T1 INNER JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T2.duration > 24 AND T1.date < '1997-01-01' ORDER BY T2.amount ASC LIMIT 1
SELECT T3.account_id FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id JOIN account AS T3 ON T1.client_id = T3.district_id WHERE T1.gender = 'F' ORDER BY T1.birth_date ASC, T2.A11 ASC LIMIT 1
SELECT COUNT(T1.client_id) FROM client AS T1 JOIN district AS T2 ON T1.district_id = T2.district_id WHERE STRFTIME('%Y', T1.birth_date) = '1920' AND T2.A3 = 'east Bohemia'
SELECT COUNT(DISTINCT T2.account_id) FROM account AS T2 JOIN disp AS T3 ON T2.account_id = T3.account_id JOIN loan AS T4 ON T2.account_id = T4.account_id WHERE T2.frequency = 'POPLATEK TYDNE' AND T4.duration = 24
SELECT AVG(T1.amount) FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.status = 'C' AND T2.frequency = 'POPLATEK PO OBRATU'
SELECT T1.client_id, T1.district_id FROM client AS T1 JOIN disp AS T2 ON T1.client_id = T2.client_id WHERE T2.type = 'OWNER'
SELECT T3.client_id, (strftime('%Y', 'now') - strftime('%Y', T3.birth_date)) AS age FROM card AS T1 JOIN disp AS T2 ON T1.disp_id = T2.disp_id JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.type = 'gold' AND T2.type = 'OWNER'
SELECT bond_type FROM bond GROUP BY bond_type ORDER BY COUNT(bond_type) DESC LIMIT 1
SELECT COUNT(*) FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '-' AND T2.element = 'cl'
SELECT AVG(CASE WHEN T1.element = 'o' THEN 1 ELSE 0 END) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '-'
SELECT AVG(CASE WHEN T2.bond_type = '-' THEN 1 ELSE 0 END) FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+'
SELECT COUNT(T1.molecule_id) FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '-' AND T2.element = 'na'
SELECT DISTINCT T2.molecule_id FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '#' AND T2.label = '+'
SELECT CAST(SUM(IIF(T1.element = 'c', 1, 0)) AS REAL) * 100 / COUNT(*) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '='
SELECT COUNT(*) FROM bond WHERE bond_type = '#'
SELECT COUNT(atom_id) FROM atom WHERE element != 'br'
SELECT COUNT(*) FROM molecule WHERE molecule_id BETWEEN 'TR000' AND 'TR099' AND label = '+'
SELECT DISTINCT T1.molecule_id FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.element = 'c'
SELECT T3.element FROM bond AS T1 JOIN connected AS T2 ON T1.bond_id = T2.bond_id JOIN atom AS T3 ON T2.atom_id = T3.atom_id WHERE T1.bond_id = 'TR004_8_9'
SELECT T2.element FROM bond AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '='
SELECT T2.label FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'h' GROUP BY T2.label ORDER BY COUNT(T2.label) DESC LIMIT 1
SELECT T2.bond_type FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'cl'
SELECT T2.atom_id, T2.atom_id2 FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T1.bond_type = '-'
SELECT T3.atom_id, T3.atom_id2 FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN connected AS T3 ON T2.bond_id = T3.bond_id WHERE T1.label = '-'
SELECT T2.element FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '-' GROUP BY T2.element ORDER BY COUNT(T2.element) ASC LIMIT 1
SELECT T1.bond_type FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE (T2.atom_id = 'TR004_8' AND T2.atom_id2 = 'TR004_20') OR (T2.atom_id = 'TR004_20' AND T2.atom_id2 = 'TR004_8')
SELECT label FROM molecule WHERE molecule_id NOT IN (SELECT molecule_id FROM atom WHERE element = 'sn')
SELECT COUNT(DISTINCT T1.atom_id) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element IN ('i', 's') AND T2.bond_type = '-'
SELECT T2.atom_id, T2.atom_id2 FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T1.bond_type = '#'
SELECT DISTINCT T4.atom_id FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id JOIN connected AS T4 ON T3.bond_id = T4.bond_id WHERE T1.molecule_id = 'TR181'
SELECT (CAST(COUNT(CASE WHEN T1.element != 'f' THEN T1.atom_id END) AS REAL) * 100) / COUNT(DISTINCT T1.atom_id) FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+'
SELECT CAST(SUM(CASE WHEN T1.bond_type = '#' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.bond_id) FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+'
SELECT DISTINCT element FROM atom WHERE molecule_id = 'TR000' ORDER BY element ASC LIMIT 3
SELECT T2.atom_id, T2.atom_id2 FROM connected AS T2 INNER JOIN bond AS T1 ON T2.bond_id = T1.bond_id WHERE T1.molecule_id = 'TR001' AND T1.bond_id = 'TR001_2_6'
SELECT (SUM(CASE WHEN label = '+' THEN 1 ELSE 0 END) - SUM(CASE WHEN label = '-' THEN 1 ELSE 0 END)) AS difference FROM molecule
SELECT atom_id, atom_id2 FROM connected WHERE bond_id = 'TR000_2_5'
SELECT bond_id FROM connected WHERE atom_id2 = 'TR000_2'
SELECT T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' ORDER BY T2.label LIMIT 5
SELECT CAST(COUNT(CASE WHEN bond_type = '=' THEN bond_id END) AS REAL) * 100 / COUNT(bond_id) FROM bond WHERE molecule_id = 'TR008'
SELECT CAST(COUNT(CASE WHEN label = '+' THEN molecule_id END) AS REAL) * 100 / COUNT(molecule_id) FROM molecule
SELECT CAST(COUNT(CASE WHEN element = 'h' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(atom_id) FROM atom WHERE molecule_id = 'TR206'
SELECT bond_type FROM bond WHERE molecule_id = 'TR000'
SELECT T1.element, T2.label FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR060'
SELECT T1.bond_type, T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.molecule_id = 'TR010' GROUP BY T1.bond_type ORDER BY COUNT(T1.bond_type) DESC LIMIT 1
SELECT DISTINCT T1.molecule_id FROM molecule AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '-' AND T1.label = '-' ORDER BY T1.molecule_id ASC LIMIT 3
SELECT T1.bond_type FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR006' ORDER BY T1.bond_type ASC LIMIT 2
SELECT COUNT(T1.bond_id) FROM bond AS T1 JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR009_12' AND T1.molecule_id = 'TR009' OR T2.atom_id2 = 'TR009_12' AND T1.molecule_id = 'TR009'
SELECT COUNT(*) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' AND T1.element = 'br'
SELECT T1.bond_type, T2.atom_id, T2.atom_id2 FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T1.bond_id = 'TR001_6_9'
SELECT T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.atom_id = 'TR001_10'
SELECT COUNT(molecule_id) FROM bond WHERE bond_type = '#'
SELECT count(*) FROM connected WHERE atom_id LIKE 'TR%_19'
SELECT T2.element FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.molecule_id = 'TR004'
SELECT COUNT(molecule_id) FROM molecule WHERE label = '-'
SELECT T1.molecule_id FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE SUBSTR(T2.atom_id, 7, 2) BETWEEN '21' AND '25' AND T1.label = '+'
SELECT T2.bond_id FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'p' OR T1.element = 'n'
SELECT T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' GROUP BY T2.molecule_id ORDER BY COUNT(T1.bond_id) DESC LIMIT 1
SELECT COUNT(*) / COUNT(DISTINCT T1.atom_id) AS average_bonds FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T2.element = 'i'
SELECT T1.bond_type, CAST(SUBSTR(T2.atom_id, 7, 2) AS INT) AS bond_id FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE CAST(SUBSTR(T2.atom_id, 7, 2) AS INT) = 45
SELECT DISTINCT T1.element FROM atom AS T1 WHERE NOT EXISTS (SELECT 1 FROM connected AS T2 WHERE T2.atom_id = T1.atom_id)
SELECT T3.element FROM molecule AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id JOIN connected AS T4 ON T2.bond_id = T4.bond_id JOIN atom AS T3 ON T4.atom_id = T3.atom_id WHERE T1.molecule_id = 'TR041' AND T2.bond_type = '#'
SELECT T1.element FROM atom AS T1 JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T2.bond_id = 'TR144_8_19'
SELECT T1.molecule_id FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+' AND T2.bond_type = '=' GROUP BY T1.molecule_id ORDER BY COUNT(T2.bond_id) DESC LIMIT 1
SELECT T1.element FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' GROUP BY T1.element ORDER BY COUNT(T1.element) ASC LIMIT 1
SELECT T1.atom_id FROM connected AS T1 JOIN bond AS T2 ON T1.bond_id = T2.bond_id JOIN atom AS T3 ON T3.atom_id = T1.atom_id2 WHERE T3.element = 'pb'
SELECT DISTINCT T2.element AS element_Bond FROM bond AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '#'
SELECT CAST(COUNT(CASE WHEN element1 <> element2 THEN bond_id ELSE NULL END) AS REAL) * 100 / COUNT(bond_id) FROM ( SELECT T2.bond_id, T1.element AS element1, T3.element AS element2 FROM atom AS T1 JOIN connected AS T4 ON T1.atom_id = T4.atom_id JOIN atom AS T3 ON T3.atom_id = T4.atom_id2 JOIN bond AS T2 ON T2.bond_id = T4.bond_id ) WHERE element1 <> element2
SELECT CAST(COUNT(CASE WHEN T2.label = '+' THEN 1 END) AS REAL) * 100 / COUNT(*) AS proportion FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '-'
SELECT COUNT(atom_id) FROM atom WHERE element IN ('c', 'h')
SELECT T2.atom_id2 FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T1.element = 's'
SELECT bond.bond_type FROM atom JOIN bond ON atom.molecule_id = bond.molecule_id WHERE atom.element = 'sn'
SELECT COUNT(DISTINCT T2.element) FROM bond AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '-'
SELECT COUNT(DISTINCT T3.atom_id) FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id INNER JOIN atom AS T3 ON T2.atom_id = T3.atom_id WHERE T1.bond_type = '#' AND T3.element IN ('p', 'br')
SELECT T2.bond_id FROM molecule AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+'
SELECT T2.molecule_id FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '-' AND T2.label = '-'
SELECT CAST(SUM(CASE WHEN T1.element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '-'
SELECT label FROM molecule WHERE molecule_id IN ('TR000', 'TR001', 'TR002')
SELECT molecule_id FROM molecule WHERE label = '-'
SELECT COUNT(molecule_id) FROM molecule WHERE molecule_id BETWEEN 'TR000' AND 'TR030' AND label = '+'
SELECT bond_type FROM bond WHERE molecule_id BETWEEN 'TR000' AND 'TR050'
SELECT T2.element FROM bond AS T1 INNER JOIN connected AS T3 ON T1.bond_id = T3.bond_id INNER JOIN atom AS T2 ON T3.atom_id = T2.atom_id WHERE T1.bond_id = 'TR001_10_11'
SELECT COUNT(1) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'i'
SELECT label FROM molecule WHERE molecule_id IN (SELECT molecule_id FROM atom WHERE element = 'ca') GROUP BY label ORDER BY COUNT(label) DESC LIMIT 1
SELECT T3.element FROM connected AS T1 JOIN bond AS T2 ON T1.bond_id = T2.bond_id JOIN atom AS T3 ON T1.atom_id = T3.atom_id WHERE T2.bond_id = 'TR001_1_8' UNION SELECT T3.element FROM connected AS T1 JOIN bond AS T2 ON T1.bond_id = T2.bond_id JOIN atom AS T3 ON T1.atom_id2 = T3.atom_id WHERE T2.bond_id = 'TR001_1_8'
SELECT DISTINCT T1.molecule_id FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN molecule AS T3 ON T1.molecule_id = T3.molecule_id WHERE T1.element = 'c' AND T2.bond_type = '#' AND T3.label = '-'
SELECT (CAST(SUM(CASE WHEN element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(atom_id) AS percentage FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '+'
SELECT DISTINCT T1.element FROM atom AS T1 WHERE T1.molecule_id = 'TR001'
SELECT molecule_id FROM bond WHERE bond_type = '='
SELECT DISTINCT T1.atom_id, T1.atom_id2 FROM connected AS T1 INNER JOIN bond AS T2 ON T1.bond_id = T2.bond_id WHERE T2.bond_type = '#'
SELECT DISTINCT T1.element FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_id = 'TR000_1_2'
SELECT COUNT(*) FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '-' AND T2.bond_type = '-'
SELECT T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_id = 'TR001_10_11'
SELECT T1.bond_id, T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '#'
SELECT T1.element FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' AND SUBSTR(T1.atom_id, 7, 1) = '4'
SELECT CAST(SUM(CASE WHEN T1.element = 'h' THEN 1 ELSE 0 END) AS REAL) / COUNT(T1.atom_id) AS HydrogenRatio, T2.label AS Carcinogenicity FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.molecule_id = 'TR006'
SELECT T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'ca'
SELECT T2.bond_type FROM atom AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'c'
SELECT T3.element FROM connected AS T1 INNER JOIN atom AS T3 ON T3.atom_id = T1.atom_id INNER JOIN bond AS T2 ON T2.bond_id = T1.bond_id WHERE T2.bond_id = 'TR001_10_11'
SELECT CAST(COUNT(CASE WHEN bond_type = '#' THEN bond_id ELSE NULL END) AS REAL) * 100 / COUNT(bond_id) FROM bond
SELECT CAST(SUM(CASE WHEN T1.bond_type = '=' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.bond_id) FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR047'
SELECT T2.label FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.atom_id = 'TR001_1' AND T2.label = '+'
SELECT label FROM molecule WHERE molecule_id = 'TR151'
SELECT T1.element FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR151'
SELECT COUNT(molecule_id) FROM molecule WHERE label = '+'
SELECT T1.atom_id FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE CAST(SUBSTR(T2.molecule_id, 3, 3) AS REAL) BETWEEN 10 AND 50 AND T1.element = 'c'
SELECT COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+'
SELECT T2.bond_id FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+' AND T2.bond_type = '='
SELECT COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' AND T1.element = 'h'
SELECT T1.molecule_id FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR000_1' AND T1.bond_id = 'TR000_1_2'
SELECT T1.atom_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '-' AND T1.element = 'c'
SELECT CAST(COUNT(CASE WHEN T2.label = '+' AND T1.element = 'h' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(T1.element) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id
SELECT label FROM molecule WHERE molecule_id = 'TR124'
SELECT atom_id FROM atom WHERE molecule_id = 'TR186'
SELECT bond_type FROM bond WHERE bond_id = 'TR007_4_19'
SELECT DISTINCT T2.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T1.bond_id = 'TR001_2_4'
SELECT COUNT(*) AS double_bond_count, T2.label FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.molecule_id = 'TR006' AND T1.bond_type = '='
SELECT T1.label, T2.element FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+'
SELECT T2.bond_id, T3.atom_id, T3.atom_id2 FROM bond AS T2 INNER JOIN connected AS T3 ON T2.bond_id = T3.bond_id WHERE T2.bond_type = '-'
SELECT DISTINCT T2.element FROM bond AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '#'
SELECT T1.element FROM atom AS T1 JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T2.bond_id = 'TR000_2_3'
SELECT COUNT(*) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'cl'
SELECT t1.atom_id, COUNT(DISTINCT t2.bond_type) AS distinct_bond_types FROM atom t1 JOIN bond t2 ON t1.molecule_id = t2.molecule_id WHERE t1.molecule_id = 'TR346'
SELECT COUNT(*) FROM bond AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' AND T2.label = '+'
SELECT COUNT(DISTINCT T1.molecule_id) FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id JOIN bond AS T3 ON T1.molecule_id = T3.molecule_id WHERE T2.element <> 's' AND T3.bond_type <> '='
SELECT T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_id = 'TR001_2_4'
SELECT COUNT(atom_id) FROM atom WHERE molecule_id = 'TR001'
SELECT COUNT(*) FROM bond WHERE bond_type = '-'
SELECT T1.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'cl' AND T2.label = '+'
SELECT DISTINCT M.molecule_id FROM molecule AS M INNER JOIN atom AS A ON M.molecule_id = A.molecule_id WHERE A.element = 'c' AND M.label = '-'
SELECT CAST(COUNT(CASE WHEN T1.element = 'cl' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+'
SELECT molecule_id FROM bond WHERE bond_id = 'TR001_1_7'
SELECT COUNT(atom_id) FROM connected WHERE bond_id = 'TR001_3_4'
SELECT T1.bond_type FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR000_1' AND T2.atom_id2 = 'TR000_2'
SELECT T3.label FROM atom AS T1 JOIN connected AS T2 ON T1.atom_id = T2.atom_id JOIN molecule AS T3 ON T1.molecule_id = T3.molecule_id WHERE T1.atom_id = 'TR000_2' AND T2.atom_id2 = 'TR000_4'
SELECT element FROM atom WHERE atom_id = 'TR000_1'
SELECT label FROM molecule WHERE molecule_id = 'TR000'
SELECT CAST(COUNT(CASE WHEN bond_type = '-' THEN bond_id END) AS REAL) * 100 / COUNT(bond_id) FROM bond
SELECT COUNT(*) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'n' AND T2.label = '+'
SELECT T1.label FROM molecule AS T1  JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id  JOIN bond AS T3 ON T1.molecule_id = T3.molecule_id  WHERE T2.element = 's' AND T3.bond_type = '='
SELECT T1.molecule_id FROM molecule AS T1 JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id GROUP BY T1.molecule_id HAVING COUNT(T2.atom_id) > 5 AND T1.label = '-'
SELECT T1.element FROM atom AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '=' AND T1.molecule_id = 'TR024'
SELECT T1.molecule_id FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+' GROUP BY T1.molecule_id ORDER BY COUNT(T2.molecule_id) DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN T3.label = '+' THEN T2.molecule_id ELSE NULL END) AS REAL) * 100.0 / COUNT(T2.molecule_id) FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN molecule AS T3 ON T1.molecule_id = T3.molecule_id WHERE T1.element = 'h' AND T2.bond_type = '#'
SELECT COUNT(molecule_id) FROM molecule WHERE label = '+'
SELECT COUNT(*) FROM bond WHERE bond_type = '-' AND molecule_id BETWEEN 'TR004' AND 'TR010'
SELECT COUNT(*) FROM atom WHERE molecule_id = 'TR008' AND element = 'c'
SELECT T1.element FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '-' AND T1.atom_id = 'TR004_7'
SELECT COUNT(DISTINCT T1.molecule_id) FROM atom AS T1 JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'o' AND T2.bond_type = '='
SELECT COUNT(T2.molecule_id) FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type LIKE '#' AND T2.label LIKE '-'
SELECT T1.element, T2.bond_type FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.molecule_id = 'TR002'
SELECT T1.atom_id FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN connected AS T3 ON T1.atom_id = T3.atom_id WHERE T1.molecule_id = 'TR012' AND T2.bond_type = '=' AND T1.element = 'c'
SELECT T1.atom_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' AND T1.element = 'o'
SELECT name FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT id FROM cards WHERE borderColor = 'borderless' AND (cardKingdomFoilId IS NULL OR cardKingdomId IS NULL)
SELECT name FROM cards ORDER BY faceConvertedManaCost DESC LIMIT 1
SELECT name FROM cards WHERE edhrecRank < 100 AND frameVersion = '2015'
SELECT T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'mythic' AND T2.format = 'gladiator' AND T2.status = 'Banned'
SELECT T2.status FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.types = 'Artifact' AND T1.side IS NULL AND T2.format = 'vintage'
SELECT T1.id, T1.artist FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE (T1.power = '*' OR T1.power IS NULL) AND T2.format = 'commander' AND T2.status = 'Legal'
SELECT T1.id, T3.text, T1.hasContentWarning FROM cards AS T1 JOIN rulings AS T3 ON T1.uuid = T3.uuid WHERE T1.artist = 'Stephen Daniele'
SELECT T2.text FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Sublime Epiphany' AND T1.number = '74s'
SELECT T2.name, T2.artist, T2.isPromo FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid GROUP BY T2.uuid ORDER BY COUNT(T1.uuid) DESC LIMIT 1
SELECT DISTINCT T2.language FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Annul' AND T1.number = '29'
SELECT T2.name FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.language = 'Japanese'
SELECT CAST(COUNT(CASE WHEN language = 'Chinese Simplified' THEN 1 END) AS REAL) * 100 / COUNT(id) FROM foreign_data
SELECT T1.name, T1.totalSetSize FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Italian'
SELECT COUNT(DISTINCT types) FROM cards WHERE artist = 'Aaron Boyd'
SELECT keywords FROM cards WHERE name = 'Angel of Mercy'
SELECT COUNT(*) FROM cards WHERE power = '*'
SELECT promoTypes FROM cards WHERE name = 'Duress'
SELECT borderColor FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT originalType FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT DISTINCT T3.language FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code JOIN set_translations AS T3 ON T2.code = T3.setCode WHERE T1.name = 'Angel of Mercy'
SELECT COUNT(T1.uuid) FROM legalities AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.status = 'Restricted' AND T2.isTextless = 0
SELECT T2.text FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Condemn'
SELECT COUNT(T1.uuid) FROM legalities AS T1 JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.status = 'Restricted' AND T2.isStarter = 1
SELECT T2.status FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Cloudchaser Eagle'
SELECT type FROM cards WHERE name = 'Benalish Knight'
SELECT T2.format FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Benalish Knight'
SELECT T1.artist FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'Phyrexian'
SELECT CAST(COUNT(CASE WHEN borderColor = 'borderless' THEN id ELSE NULL END) AS REAL) * 100 / COUNT(id) FROM cards
SELECT COUNT(T1.id) FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'German' AND T1.isReprint = 1
SELECT COUNT(*) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.borderColor = 'borderless' AND T2.language = 'Russian'
SELECT CAST(SUM(CASE WHEN T2.language = 'French' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.isStorySpotlight = 1
SELECT COUNT(*) FROM cards WHERE toughness = 99
SELECT name FROM cards WHERE artist = 'Aaron Boyd'
SELECT COUNT(id) FROM cards WHERE borderColor = 'black' AND availability = 'mtgo'
SELECT id FROM cards WHERE convertedManaCost = 0
SELECT layout FROM cards WHERE keywords LIKE '%Flying%'
SELECT COUNT(*) FROM cards WHERE originalType = 'Summon - Angel' AND subtypes != 'Angel'
SELECT id FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT id FROM cards WHERE duelDeck = 'a'
SELECT edhrecRank FROM cards WHERE frameVersion = '2015'
SELECT T1.artist FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'Chinese Simplified'
SELECT T1.name FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.availability LIKE 'paper' AND T2.language LIKE 'Japanese'
SELECT COUNT(*) FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T2.status = 'Banned' AND T1.borderColor = 'white'
SELECT T1.uuid, T3.language FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid JOIN foreign_data AS T3 ON T1.uuid = T3.uuid WHERE T2.format = 'legacy'
SELECT T1.text FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.name = 'Beacon of Immortality'
SELECT COUNT(T1.id) FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.frameVersion = 'future' AND T2.status = 'Legal'
SELECT T2.name, T2.colors FROM set_translations AS T1 INNER JOIN cards AS T2 ON T1.setCode = T2.setCode WHERE T1.setCode = 'OGW'
SELECT cards.name, set_translations.translation, set_translations.language  FROM cards  INNER JOIN sets ON cards.setCode = sets.code  INNER JOIN foreign_data ON cards.uuid = foreign_data.uuid  INNER JOIN set_translations ON sets.code = set_translations.setCode  WHERE cards.setCode = '10E' AND cards.convertedManaCost = 5
SELECT T1.name, T2.date FROM cards AS T1 JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.originalType = 'Creature - Elf'
SELECT T1.colors, T2.format FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.id BETWEEN 1 AND 20
SELECT T1.name FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.originalType = 'Artifact' AND T1.colors = 'B'
SELECT T1.name FROM cards AS T1 JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'uncommon' ORDER BY T2.date ASC LIMIT 3
SELECT COUNT(id) FROM cards WHERE artist = 'John Avon' AND cardKingdomFoilId IS NOT NULL
SELECT COUNT(*) FROM cards WHERE borderColor = 'white' AND cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT COUNT(*) FROM cards WHERE artist = 'UDON' AND availability = 'mtgo' AND hand = -1
SELECT COUNT(id) FROM cards WHERE frameVersion = '1993' AND availability = 'paper' AND hasContentWarning = 1
SELECT manaCost  FROM cards  WHERE availability = 'mtgo,paper'    AND frameVersion = '2003'    AND borderColor = 'black'    AND layout = 'normal'
SELECT SUM(convertedManaCost) FROM cards WHERE artist = 'Rob Alexander'
SELECT subtypes, supertypes FROM cards WHERE availability = 'arena'
SELECT T1.code FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Spanish'
SELECT CAST(COUNT(CASE WHEN isOnlineOnly = 1 THEN 1 END) AS REAL) * 100 / COUNT(id) AS percentage FROM cards WHERE frameEffects = 'legendary'
SELECT CAST(SUM(CASE WHEN isStorySpotlight = 1 AND isTextless = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM cards
SELECT CAST(SUM(CASE WHEN T2.language = 'Spanish' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.baseSetSize = 309
SELECT COUNT(*) FROM sets AS s JOIN set_translations AS st ON s.code = st.setCode WHERE s.block = 'Commander' AND st.language = 'Portuguese (Brasil)'
SELECT T1.id FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.types = 'Creature' AND T2.status = 'Legal'
SELECT T2.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.subtypes IS NOT NULL AND T1.supertypes IS NOT NULL
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND text LIKE '%triggered ability%'
SELECT COUNT(*) FROM cards AS T1 JOIN rulings AS T2 ON T1.uuid = T2.uuid JOIN legalities AS T3 ON T1.uuid = T3.uuid WHERE T3.format = 'premodern' AND T2.text = 'This is a triggered mana ability.' AND T1.side IS NULL
SELECT T1.id FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.availability = 'paper' AND T2.format = 'pauper' AND T1.artist = 'Erica Yang'
SELECT T1.artist FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.text = 'Das perfekte Gegenmittel zu einer dichten Formation'
SELECT T2.name FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.artist = 'Matthew D. Wilson' AND T1.borderColor = 'black' AND T1.layout = 'normal' AND T2.language = 'French' AND T1.type LIKE '%Creature%'
SELECT COUNT(*) FROM cards AS T1 JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'rare' AND T2.`date` = '2007-02-01'
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.baseSetSize = 180 AND T1.block = 'Ravnica'
SELECT CAST(SUM(CASE WHEN T1.hasContentWarning = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T2.format = 'commander' AND T2.status = 'Legal'
SELECT (CAST(COUNT(CASE WHEN T2.language = 'French' THEN 1 ELSE NULL END) AS REAL) * 100) / COUNT(T2.language) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.power IS NULL OR T1.power = '*'
SELECT CAST(COUNT(CASE WHEN T2.language = 'Japanese' THEN T1.id ELSE NULL END) AS REAL) * 100 / COUNT(T1.id) FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.type = 'expansion'
SELECT availability FROM cards WHERE artist = 'Daren Bader'
SELECT COUNT(*) FROM cards WHERE borderColor = 'borderless' AND edhrecRank > 12000
SELECT COUNT(id) FROM cards WHERE isOversized = 1 AND isReprint = 1 AND isPromo = 1
SELECT name FROM cards WHERE (power IS NULL OR power = '*') AND promoTypes LIKE 'arenaleague' ORDER BY name ASC LIMIT 3
SELECT language FROM foreign_data WHERE multiverseid = 149934
SELECT cardKingdomFoilId, cardKingdomId FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL ORDER BY cardKingdomFoilId ASC LIMIT 3
SELECT CAST(COUNT(CASE WHEN isTextless = 1 AND layout = 'normal' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM cards
SELECT T1.number FROM cards AS T1 WHERE T1.otherFaceIds IS NULL AND T1.subtypes LIKE '%Angel%' AND T1.subtypes LIKE '%Wizard%'
SELECT name FROM sets WHERE mtgoCode IS NULL OR mtgoCode = '' ORDER BY name LIMIT 3
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Archenemy' AND T1.code = 'ARC'
SELECT T1.name, T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.id = 5
SELECT T1.translation, T2.type FROM set_translations AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.id = 206
SELECT T1.name, T1.id FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Italian' AND T1.block = 'Shadowmoor' ORDER BY T1.name ASC LIMIT 2
SELECT T1.id FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.isForeignOnly = 0 AND T1.isFoilOnly = 1
SELECT T1.name FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Russian' ORDER BY T1.baseSetSize DESC LIMIT 1
SELECT SUM(CASE WHEN T2.language = 'Chinese Simplified' THEN 1 ELSE NULL END) * 100.0 / COUNT(T1.id) FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.isOnlineOnly = 1
SELECT COUNT(*) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.`language` = 'Japanese' AND (T1.mtgoCode IS NULL OR T1.mtgoCode = '')
SELECT COUNT(id) FROM cards WHERE borderColor = 'black'
SELECT COUNT(id) FROM cards WHERE frameEffects = 'extendedart'
SELECT name FROM cards WHERE borderColor = 'black' AND isFullArt = 1
SELECT T2.translation FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.id = 174
SELECT name FROM sets WHERE code = 'ALL'
SELECT T1.language FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'A Pedra Fellwar'
SELECT code FROM sets WHERE releaseDate = '2007-07-13'
SELECT baseSetSize, code FROM sets WHERE block IN ('Masques', 'Mirage')
SELECT code FROM sets WHERE TYPE = 'expansion'
SELECT T2.name, T2.type FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.watermark = 'boros'
SELECT T2.language, T2.flavorText, T1.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.watermark = 'colorpie'
SELECT CAST(COUNT(CASE WHEN T1.convertedManaCost = 10 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 WHERE T1.name = 'Abyssal Horror'
SELECT code FROM sets WHERE type = 'expansion'
SELECT T1.name, T1.type FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.watermark = 'abzan'
SELECT T2.language, T1.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.watermark = 'azorius'
SELECT COUNT(*) FROM cards WHERE artist = 'Aaron Miller' AND cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT COUNT(*) FROM cards WHERE availability LIKE '%paper%' AND hand = '3'
SELECT name FROM cards WHERE isTextless = 0
SELECT manaCost FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT COUNT(*) FROM cards WHERE borderColor = 'white' AND (power = '*' OR power IS NULL)
SELECT name FROM cards WHERE isPromo = 1 AND side IS NOT NULL
SELECT subtypes, supertypes FROM cards WHERE name = 'Molimo, Maro-Sorcerer'
SELECT purchaseUrls FROM cards WHERE promoTypes = 'bundle'
SELECT COUNT(DISTINCT artist) FROM cards WHERE borderColor = 'black' AND availability LIKE '%arena,mtgo%'
SELECT name FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1
SELECT artist FROM cards WHERE flavorName = 'Battra, Dark Destroyer'
SELECT name FROM cards WHERE frameVersion = '2003' ORDER BY convertedManaCost DESC LIMIT 3
SELECT T3.translation FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code JOIN set_translations AS T3 ON T2.code = T3.setCode WHERE T1.name = 'Ancestor''s Chosen' AND T3.language = 'Italian'
SELECT COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code INNER JOIN set_translations AS T3 ON T2.code = T3.setCode WHERE T1.name = 'Angel of Mercy'
SELECT cards.name FROM cards INNER JOIN sets ON cards.setCode = sets.code INNER JOIN set_translations ON sets.code = set_translations.setCode WHERE set_translations.translation = 'Hauptset Zehnte Edition'
SELECT CASE WHEN EXISTS (SELECT 1 FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Ancestor''s Chosen' AND T2.language = 'Korean') THEN 1 ELSE 0 END
SELECT COUNT(T3.id) FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode JOIN cards AS T3 ON T3.setCode = T2.setCode WHERE T2.translation = 'Hauptset Zehnte Edition' AND T3.artist = 'Adam Rex'
SELECT T1.baseSetSize FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Hauptset Zehnte Edition'
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Eighth Edition' AND T2.language = 'Chinese Simplified'
SELECT CASE WHEN EXISTS (SELECT 1 FROM cards AS T1 INNER JOIN sets AS T2 ON T1.mtgoId = T2.id WHERE T1.name = 'Angel of Mercy' AND T2.mtgoCode IS NOT NULL) THEN 'Yes' ELSE 'No' END
SELECT T2.releaseDate FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Ancestor''s Chosen'
SELECT T1.type FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Hauptset Zehnte Edition'
SELECT COUNT(*) FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.block = 'Ice Age' AND T2.language = 'Italian' AND T2.translation IS NOT NULL
SELECT T2.isForeignOnly FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Adarkar Valkyrie'
SELECT COUNT(*) FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language LIKE 'Italian' AND T1.baseSetSize < 100
SELECT COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T2.code = T1.setCode WHERE T2.name = 'Coldsnap' AND T1.borderColor = 'black'
SELECT T1.name FROM cards AS T1 JOIN sets AS T2 ON T2.code = T1.setCode WHERE T2.name = 'Coldsnap' ORDER BY T1.convertedManaCost DESC LIMIT 1
SELECT T1.artist FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap' AND T1.artist IN ('Jeremy Jarvis', 'Aaron Miller', 'Chippy')
SELECT T1.number FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap' AND T1.number = 4
SELECT COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap' AND T1.convertedManaCost > 5 AND (T1.power IS NULL OR T1.power = '*')
SELECT T2.flavorText FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'Italian' AND T1.name = 'Ancestor''s Chosen'
SELECT DISTINCT T1.language FROM foreign_data AS T1 JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.name = 'Ancestor''s Chosen' AND T1.flavorText IS NOT NULL
SELECT T2.type FROM cards AS T1 JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Ancestor''s Chosen' AND T2.language = 'German'
SELECT T2.text FROM sets AS T1 JOIN cards AS T3 ON T1.code = T3.setCode JOIN rulings AS T2 ON T3.uuid = T2.uuid WHERE T1.name = 'Coldsnap' AND EXISTS (SELECT 1 FROM set_translations WHERE setCode = T1.code AND language = 'Italian')
SELECT T3.name FROM sets AS T1 JOIN cards AS T2 ON T1.code = T2.setCode JOIN foreign_data AS T3 ON T2.uuid = T3.uuid WHERE T1.name = 'Coldsnap' ORDER BY T2.convertedManaCost DESC LIMIT 1
SELECT T1.date FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.name = 'Reminisce'
SELECT CAST(SUM(CASE WHEN T1.convertedManaCost = 7 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap'
SELECT CAST(SUM(CASE WHEN cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap'
SELECT code FROM sets WHERE releaseDate = '2017-07-14'
SELECT keyruneCode FROM sets WHERE code = 'PKHC'
SELECT mcmId FROM sets WHERE code = 'SS2'
SELECT mcmName FROM sets WHERE releaseDate = '2017-06-09'
SELECT type FROM sets WHERE name LIKE 'From the Vault: Lore'
SELECT parentCode FROM sets WHERE name = 'Commander 2014 Oversized'
SELECT T1.text, T2.hasContentWarning FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.artist = 'Jim Pavelec'
SELECT T2.releaseDate FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Evacuation'
SELECT T1.baseSetSize FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Rinascita di Alara'
SELECT T1.type FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Huitième édition'
SELECT T3.translation FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code INNER JOIN set_translations AS T3 ON T2.code = T3.setCode WHERE T1.name = 'Tendo Ice Bridge'
SELECT COUNT(T2.translation) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Tenth Edition'
SELECT T1.translation FROM set_translations AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code INNER JOIN cards AS T3 ON T2.code = T3.setCode WHERE T3.name = 'Fellwar Stone' AND T1.language = 'Japanese'
SELECT T1.name FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Journey into Nyx Hero''s Path' ORDER BY T1.convertedManaCost DESC LIMIT 1
SELECT T1.releaseDate FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Ola de frío'
SELECT T2.type FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Samite Pilgrim'
SELECT COUNT(*) FROM sets AS T1 JOIN cards AS T2 ON T1.code = T2.setCode WHERE T1.name = 'World Championship Decks 2004' AND T2.convertedManaCost = 3
SELECT T2.translation FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Mirrodin' AND T2.language = 'Chinese Simplified'
SELECT CAST(COUNT(CASE WHEN T1.isNonFoilOnly = 1 THEN T1.id ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Japanese'
SELECT CAST(SUM(CASE WHEN T2.isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.language = 'Portuguese (Brazil)'
SELECT T1.availability FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.isTextless = 1 AND T1.artist = 'Aleksi Briclot'
SELECT id FROM sets ORDER BY baseSetSize DESC LIMIT 1
SELECT artist FROM cards WHERE side IS NULL ORDER BY convertedManaCost DESC LIMIT 1
SELECT frameEffects FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL GROUP BY frameEffects ORDER BY COUNT(frameEffects) DESC LIMIT 1
SELECT COUNT(id) FROM cards WHERE (power IS NULL OR power = '*') AND hasFoil = 0 AND duelDeck = 'a'
SELECT id FROM sets WHERE type = 'commander' ORDER BY totalSetSize DESC LIMIT 1
SELECT T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T2.format = 'duel' AND T1.manaCost IS NOT NULL ORDER BY T1.convertedManaCost DESC LIMIT 10
SELECT cards.originalReleaseDate, GROUP_CONCAT(DISTINCT CASE WHEN legalities.status = 'Legal' THEN legalities.format ELSE NULL END) FROM cards INNER JOIN legalities ON cards.uuid = legalities.uuid WHERE cards.rarity = 'mythic' ORDER BY cards.originalReleaseDate ASC LIMIT 1
SELECT COUNT(*) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.artist = 'Volkan Baǵa' AND T2.language = 'French'
SELECT COUNT(*) FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'rare' AND T1.types = 'Enchantment' AND T1.name = 'Abundance' AND T2.status = 'Legal'
SELECT T2.format, T1.name FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T2.status = 'Banned' GROUP BY T2.format ORDER BY COUNT(CASE WHEN T2.status = 'Banned' THEN T1.id ELSE NULL END) DESC LIMIT 1
SELECT T2.language FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Battlebond'
SELECT T1.artist, T2.format FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid GROUP BY T1.artist ORDER BY COUNT(*) ASC LIMIT 1
SELECT T2.status FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.frameVersion = '1997' AND T1.artist = 'D. Alexander Gregory' AND T1.hasContentWarning = 1 AND T2.format = 'legacy'
SELECT T1.name, T2.format FROM cards AS T1 JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.edhrecRank = 1 AND T2.status = 'Banned'
-- Part 1: Calculate the average number of sets released per year SELECT AVG(CASE WHEN STRFTIME('%Y', T1.releaseDate) BETWEEN '2012' AND '2015' THEN 1 ELSE 0 END) AS avg_sets_per_year FROM sets AS T1  -- Part 2: Identify the common language SELECT T2.language FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE STRFTIME('%Y', T1.releaseDate) BETWEEN '2012' AND '2015' GROUP BY T2.language ORDER BY COUNT(T2.language) DESC LIMIT 1
SELECT artist FROM cards WHERE borderColor = 'black' AND availability = 'arena'
SELECT uuid FROM legalities WHERE format = 'oldschool' AND status IN ('Banned', 'Restricted')
SELECT COUNT(*) FROM cards WHERE artist = 'Matthew D. Wilson' AND availability = 'paper'
SELECT T2.text FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.artist = 'Kev Walker' ORDER BY T2.date DESC
SELECT T2.name, T3.format FROM sets AS T1 INNER JOIN cards AS T2 ON T2.setCode = T1.code INNER JOIN legalities AS T3 ON T2.uuid = T3.uuid WHERE T1.name = 'Hour of Devastation' AND T3.status = 'Legal'
SELECT T1.name FROM sets AS T1 JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Korean' AND T2.language NOT LIKE '%Japanese%'
SELECT T1.frameVersion, T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.artist = 'Allen Williams' AND T2.status = 'Banned'
SELECT DisplayName FROM users WHERE DisplayName IN ('Harlan', 'Jarrod Dixon') ORDER BY Reputation DESC LIMIT 1
SELECT DisplayName FROM users WHERE strftime('%Y', CreationDate) = '2011'
SELECT COUNT(Id) FROM users WHERE LastAccessDate > '2014-09-01'
SELECT DisplayName FROM users ORDER BY Views DESC LIMIT 1
SELECT COUNT(Id) FROM users WHERE Upvotes > 100 AND Downvotes > 1
SELECT COUNT(Id) FROM users WHERE Views > 10 AND strftime('%Y', CreationDate) > '2013'
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT T2.Title FROM users AS T1 INNER JOIN posts AS T2 ON T1.Id = T2.OwnerUserId WHERE T1.DisplayName = 'csgillespie'
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Title = 'Eliciting priors from experts'
SELECT T1.Title FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie' ORDER BY T1.ViewCount DESC LIMIT 1
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id ORDER BY T1.FavoriteCount DESC LIMIT 1
SELECT SUM(T1.CommentCount) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT AnswerCount FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie' ORDER BY AnswerCount DESC LIMIT 1
SELECT DISTINCT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T1.Title = 'Examples for teaching: Correlation does not mean causation'
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie' AND T1.ParentId IS NULL
SELECT DISTINCT u.DisplayName FROM users u INNER JOIN posts p ON u.Id = p.OwnerUserId WHERE p.ClosedDate IS NOT NULL
SELECT COUNT(posts.Id) FROM posts JOIN users ON posts.OwnerUserId = users.Id WHERE users.Age > 65 AND posts.Score >= 20
SELECT T2.Location FROM posts AS T1 JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Title = 'Eliciting priors from experts'
SELECT T2.Body FROM tags AS T1 INNER JOIN posts AS T2 ON T1.ExcerptPostId = T2.Id WHERE T1.TagName = 'bayesian'
SELECT T1.Body FROM posts AS T1 JOIN tags AS T2 ON T1.Id = T2.ExcerptPostId ORDER BY T2.Count DESC LIMIT 1
SELECT COUNT(T2.Id) FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'csgillespie'
SELECT T1.Name FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT COUNT(T2.Id) FROM users AS T1 JOIN badges AS T2 ON T2.UserId = T1.Id WHERE T1.DisplayName = 'csgillespie' AND STRFTIME('%Y', T2.Date) = '2011'
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T1.UserId ORDER BY COUNT(T1.Id) DESC LIMIT 1
SELECT AVG(T1.Score) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT CAST(SUM(CASE WHEN T2.Id IS NOT NULL THEN 1 ELSE 0 END) AS REAL) / COUNT(DISTINCT T1.Id) FROM users AS T1 LEFT JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Views > 200
SELECT CAST(COUNT(CASE WHEN T2.Age > 65 THEN T1.Id ELSE NULL END) AS REAL) * 100 / COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Score > 5
SELECT COUNT(*) FROM votes WHERE UserId = 58 AND CreationDate = '2010-07-19'
SELECT CreationDate FROM votes GROUP BY CreationDate ORDER BY COUNT(Id) DESC LIMIT 1
SELECT COUNT(Id) FROM badges WHERE Name = 'Revival'
SELECT T2.Title FROM comments AS T1 JOIN posts AS T2 ON T1.PostId = T2.Id ORDER BY T1.Score DESC LIMIT 1
SELECT COUNT(T1.PostId) FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T2.ViewCount = 1910
SELECT T2.FavoriteCount FROM comments AS T1 JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T1.CreationDate = '2014-04-23 20:29:39.0' AND T1.UserId = 3025
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.ParentId = 107829 AND T1.CommentCount = 1 LIMIT 1
SELECT CASE WHEN T2.ClosedDate IS NULL THEN 'well-finished' ELSE 'not well-finished' END AS PostStatus FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T1.UserId = 23853 AND T1.CreationDate = '2013-07-12 09:08:18.0'
SELECT T2.Reputation FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Id = 65041
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Tiago Pasqualini'
SELECT T2.DisplayName FROM votes AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Id = 6347
SELECT COUNT(T2.PostId) FROM posts AS T1 JOIN votes AS T2 ON T1.Id = T2.PostId WHERE T1.Title LIKE '%data visualization%'
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'DatEpicCoderGuyWhoPrograms'
SELECT CAST(COUNT(posts.Id) AS REAL) / COUNT(votes.Id) FROM posts JOIN votes ON posts.Id = votes.PostId WHERE posts.OwnerUserId = 24 AND votes.UserId = 24
SELECT ViewCount FROM posts WHERE Title = 'Integration of Weka and/or RapidMiner into Informatica PowerCenter/Developer'
SELECT Text FROM comments WHERE Score = 17
SELECT DisplayName FROM users WHERE WebsiteUrl = 'http://stackoverflow.com'
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'SilentGhost'
SELECT T2.DisplayName FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Text = 'thank you user93!'
SELECT T1.Text FROM comments AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'A Lion'
SELECT T2.DisplayName, T2.Reputation FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Title = 'Understanding what Dassault iSight is doing?'
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.Title = 'How does gentle boosting differ from AdaBoost?'
SELECT DISTINCT T1.DisplayName FROM users AS T1 JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T2.Name = 'Necromancer'
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T1.Title = 'Open source tools for visualizing multi-dimensional data'
SELECT T1.Title FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T2.DisplayName = 'Vebjorn Ljosa'
SELECT SUM(posts.Score), users.WebsiteUrl FROM posts JOIN users ON posts.LastEditorUserId = users.Id WHERE users.DisplayName = 'Yevgeny'
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.Title = 'Why square the difference instead of taking the absolute value in standard deviation?'
SELECT SUM(T2.BountyAmount) FROM posts AS T1 INNER JOIN votes AS T2 ON T1.Id = T2.PostId WHERE T1.Title LIKE '%data%'
SELECT T1.DisplayName FROM users AS T1 JOIN votes AS T2 ON T1.Id = T2.UserId JOIN posts AS T3 ON T2.PostId = T3.Id WHERE T2.BountyAmount = 50 AND T3.Title LIKE '%variance%'
SELECT AVG(posts.ViewCount), posts.Title, comments.Text FROM posts INNER JOIN tags ON posts.Tags LIKE '%' || tags.TagName || '%' INNER JOIN comments ON posts.Id = comments.PostId WHERE tags.TagName = 'humor'
SELECT COUNT(Id) FROM comments WHERE UserId = 13
SELECT Id FROM users WHERE Reputation = ( SELECT MAX(Reputation) FROM users )
SELECT Id FROM users ORDER BY Views ASC LIMIT 1
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Supporter' AND strftime('%Y', Date) = '2011'
SELECT COUNT(UserId) FROM badges GROUP BY UserId HAVING COUNT(Name) > 5
SELECT COUNT(DISTINCT T1.UserId) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Location = 'New York' AND T1.Name IN ('Supporter', 'Teacher')
SELECT T2.DisplayName, T2.Reputation FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Id = 1
SELECT T1.DisplayName FROM users AS T1 JOIN posts AS T2 ON T1.Id = T2.OwnerUserId JOIN postHistory AS T3 ON T3.PostId = T2.Id WHERE T2.ViewCount >= 1000 GROUP BY T1.Id HAVING COUNT(DISTINCT T3.PostId) = 1
SELECT T2.Name FROM comments AS T1 INNER JOIN badges AS T2 ON T1.UserId = T2.UserId GROUP BY T1.UserId ORDER BY COUNT(T1.Id) DESC LIMIT 1
SELECT COUNT(users.Id) FROM users INNER JOIN badges ON users.Id = badges.UserId WHERE badges.Name = 'Teacher' AND users.Location = 'India'
SELECT (SUM(CASE WHEN strftime('%Y', T1.Date) = '2010' THEN 1 ELSE 0 END) - SUM(CASE WHEN strftime('%Y', T1.Date) = '2011' THEN 1 ELSE 0 END)) * 100.0 / (SUM(CASE WHEN strftime('%Y', T1.Date) = '2011' THEN 1 ELSE 0 END)) AS PercentageDifference FROM badges AS T1 WHERE T1.Name = 'Student'
SELECT PostHistoryTypeId FROM postHistory WHERE PostId = 3720 UNION ALL SELECT COUNT(DISTINCT UserId) FROM comments WHERE PostId = 3720
SELECT T2.Title, T2.ViewCount FROM postLinks AS T1 INNER JOIN posts AS T2 ON T1.RelatedPostId = T2.Id WHERE T1.PostId = 61217
SELECT T2.Score, T1.LinkTypeId FROM postLinks AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T1.PostId = 395
SELECT Id, OwnerUserId FROM posts WHERE Score > 60
SELECT SUM(FavoriteCount) FROM posts WHERE OwnerUserId = 686 AND STRFTIME('%Y', CreaionDate) = '2011'
SELECT AVG(T2.UpVotes), AVG(T2.Age) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id GROUP BY T1.OwnerUserId HAVING COUNT(T1.Id) > 10
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Announcer'
SELECT Name FROM badges WHERE `Date` = '2010-07-19 19:39:08.0'
SELECT COUNT(*) FROM comments WHERE Score > 60
SELECT Text FROM comments WHERE CreationDate = '2010-07-19 19:25:47.0'
SELECT COUNT(*) FROM posts WHERE Score = 10
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Reputation = ( SELECT MAX(Reputation) FROM users )
SELECT T1.Reputation FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T2.Date = '2010-07-19 19:39:08.0'
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'Pierre'
SELECT T1.Date FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Location = 'Rochester, NY'
SELECT (CAST(COUNT(CASE WHEN Name = 'Teacher' THEN UserId ELSE NULL END) AS REAL) * 100) / COUNT(UserId) AS percentage FROM badges
SELECT (CAST(SUM(CASE WHEN T2.Age BETWEEN 13 AND 18 THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(T2.Id) FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'Organizer'
SELECT Score FROM comments WHERE CreationDate = '2010-07-19 19:19:56.0'
SELECT Text FROM comments WHERE CreationDate = '2010-07-19 19:37:33.0'
SELECT T1.Age FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Location = 'Vienna, Austria'
SELECT COUNT(T2.Id) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'Supporter' AND T2.Age BETWEEN 19 AND 65
SELECT T2.Views FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Date = '2010-07-19 19:39:08.0'
SELECT DISTINCT T2.Name FROM users AS T1 JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Reputation = ( SELECT MIN(Reputation) FROM users )
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'Sharpie'
SELECT COUNT(T2.Id) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'Supporter' AND T2.Age > 65
SELECT DisplayName FROM users WHERE Id = 30
SELECT COUNT(Id) FROM users WHERE Location = 'New York'
SELECT COUNT(*) FROM votes WHERE STRFTIME('%Y', CreationDate) = '2010'
SELECT COUNT(Id) FROM users WHERE Age BETWEEN 19 AND 65
SELECT DisplayName FROM users WHERE Views = (SELECT MAX(Views) FROM users)
SELECT CAST(COUNT(CASE WHEN STRFTIME('%Y', CreationDate) = '2010' THEN 1 ELSE NULL END) AS REAL) / COUNT(CASE WHEN STRFTIME('%Y', CreationDate) = '2011' THEN 1 ELSE NULL END) FROM votes
SELECT T2.TagName FROM posts AS T1 INNER JOIN tags AS T2 ON T1.Tags LIKE '%' || T2.TagName || '%' INNER JOIN users AS T3 ON T1.OwnerUserId = T3.Id WHERE T3.DisplayName = 'John Salvatier'
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerDisplayName = T2.DisplayName WHERE T2.DisplayName = 'Daniel Vassallo'
SELECT COUNT(T2.Id) FROM users AS T1 INNER JOIN votes AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'Harlan'
SELECT T1.Id FROM posts AS T1 JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'slashnick' ORDER BY T1.AnswerCount DESC LIMIT 1
SELECT T1.Title FROM posts AS T1 JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Harvey Motulsky' OR T2.DisplayName = 'Noah Snyder' ORDER BY T1.ViewCount DESC LIMIT 1
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id INNER JOIN votes AS T3 ON T1.Id = T3.PostId WHERE T2.DisplayName = 'Matt Parker' AND T3.PostId > 4
SELECT COUNT(T1.Score) FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Neil McGuigan' AND T1.Score < 60
SELECT DISTINCT p.Tags FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Mark Meckes' AND p.CommentCount = 0
SELECT T2.DisplayName FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'Organizer'
SELECT CAST(SUM(CASE WHEN T2.TagName = 'r' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM posts AS T1 INNER JOIN users AS T3 ON T1.OwnerUserId = T3.Id INNER JOIN posts AS T4 ON T4.Id = T1.Id INNER JOIN tags AS T2 ON T2.ExcerptPostId = T4.Id WHERE T3.DisplayName = 'Community'
SELECT (SUM(CASE WHEN users.DisplayName = 'Mornington' THEN posts.ViewCount ELSE 0 END) - SUM(CASE WHEN users.DisplayName = 'Amos' THEN posts.ViewCount ELSE 0 END)) AS ViewCountDifference FROM posts INNER JOIN users ON posts.OwnerUserId = users.Id
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Commentator' AND STRFTIME('%Y', Date) = '2014'
SELECT COUNT(Id) FROM posts WHERE CreaionDate BETWEEN '2010-07-21 00:00:00' AND '2010-07-21 23:59:59'
SELECT DisplayName, Age FROM users WHERE Views = ( SELECT MAX(Views) FROM users )
SELECT LastEditDate, LastEditorUserId FROM posts WHERE Title = 'Detecting a given face in a database of facial images'
SELECT COUNT(Id) FROM comments WHERE Score < 60 AND UserId = 13
SELECT p.Title, c.UserDisplayName FROM comments AS c INNER JOIN posts AS p ON c.PostId = p.Id WHERE c.Score > 60
SELECT T1.Name FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE strftime('%Y', T1.Date) = '2011' AND T2.Location = 'North Pole'
SELECT T2.DisplayName, T2.WebsiteUrl FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.FavoriteCount > 150
SELECT COUNT(*) AS PostHistoryCount, ( SELECT LastEditDate FROM posts WHERE Title = 'What is the best introductory Bayesian statistics textbook?' ) AS LastEditDate FROM postHistory INNER JOIN posts ON postHistory.PostId = posts.Id WHERE posts.Title = 'What is the best introductory Bayesian statistics textbook?'
SELECT T2.LastAccessDate, T2.Location FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'outliers'
SELECT T3.Title FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId INNER JOIN posts AS T3 ON T2.RelatedPostId = T3.Id WHERE T1.Title = 'How to tell if something happened in a data set which monitors a value over time'
SELECT T2.PostId, T1.Name FROM badges AS T1 INNER JOIN comments AS T2 ON T1.UserId = T2.UserId INNER JOIN users AS T3 ON T2.UserId = T3.Id WHERE T3.DisplayName = 'Samuel' AND STRFTIME('%Y', T2.CreationDate) = '2013' AND STRFTIME('%Y', T1.Date) = '2013'
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id ORDER BY T1.ViewCount DESC LIMIT 1
SELECT T3.DisplayName, T3.Location FROM tags AS T1 INNER JOIN posts AS T2 ON T1.ExcerptPostId = T2.Id INNER JOIN users AS T3 ON T2.OwnerUserId = T3.Id WHERE T1.TagName = 'hypothesis-testing'
SELECT T1.Title, T2.LinkTypeId FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId WHERE T1.Title = 'What are principal component scores?'
SELECT T1.DisplayName FROM users AS T1 JOIN posts AS T2 ON T1.Id = T2.OwnerUserId WHERE T2.ParentId IS NOT NULL ORDER BY T2.Score DESC LIMIT 1
SELECT T2.DisplayName, T2.WebsiteUrl FROM votes AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.VoteTypeId = 8 ORDER BY T1.BountyAmount DESC LIMIT 1
SELECT Title FROM posts ORDER BY ViewCount DESC LIMIT 5
SELECT COUNT(Id) FROM tags WHERE Count BETWEEN 5000 AND 7000
SELECT OwnerUserId FROM posts ORDER BY FavoriteCount DESC LIMIT 1
SELECT Age FROM users ORDER BY Reputation DESC LIMIT 1
SELECT COUNT(posts.Id) FROM posts INNER JOIN votes ON posts.Id = votes.PostId WHERE STRFTIME('%Y', votes.CreationDate) = '2011' AND votes.BountyAmount = 50
SELECT Id FROM users ORDER BY Age ASC LIMIT 1
SELECT SUM(Score) FROM posts WHERE LasActivityDate LIKE '2010-07-19%'
SELECT CAST(COUNT(T2.Id) AS REAL) / 12 FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId WHERE T1.AnswerCount <= 2 AND STRFTIME('%Y', T1.CreaionDate) = '2010'
SELECT p.Id FROM posts p JOIN votes v ON p.Id = v.PostId WHERE v.UserId = 1465 ORDER BY p.FavoriteCount DESC LIMIT 1
SELECT T1.Title FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId ORDER BY T2.CreationDate ASC LIMIT 1
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T1.UserId ORDER BY COUNT(T1.Name) DESC LIMIT 1
SELECT MIN(T1.CreationDate) FROM votes AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'chl' ORDER BY T1.CreationDate ASC LIMIT 1
SELECT T2.CreaionDate FROM users AS T1 INNER JOIN posts AS T2 ON T1.Id = T2.OwnerUserId ORDER BY T1.Age ASC, T2.CreaionDate ASC LIMIT 1
SELECT T2.DisplayName FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'Autobiographer' ORDER BY T1.Date ASC LIMIT 1
SELECT COUNT(DISTINCT users.Id) FROM posts AS posts INNER JOIN users AS users ON posts.OwnerUserId = users.Id WHERE users.Location = 'United Kingdom' AND posts.FavoriteCount >= 4
SELECT AVG(votes.PostId) FROM votes JOIN users ON votes.UserId = users.Id WHERE users.Age = (SELECT MAX(Age) FROM users)
SELECT DisplayName FROM users ORDER BY Reputation DESC LIMIT 1
SELECT COUNT(*) FROM users WHERE Reputation > 2000 AND Views > 1000
SELECT DisplayName FROM users WHERE Age BETWEEN 19 AND 65
SELECT COUNT(*) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Jay Stevens' AND strftime('%Y', T1.CreaionDate) = '2010'
SELECT T1.Id, T1.Title FROM posts AS T1 JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Harvey Motulsky' ORDER BY T1.ViewCount DESC LIMIT 1
SELECT Id, Title FROM posts ORDER BY Score DESC LIMIT 1
SELECT AVG(T1.Score) FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Stephen Turner'
SELECT T2.DisplayName FROM posts AS T1 JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.ViewCount > 20000 AND STRFTIME('%Y', T1.CreaionDate) = '2011'
SELECT T1.Id, T1.OwnerDisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE STRFTIME('%Y', T1.CreaionDate) = '2010' ORDER BY T1.FavoriteCount DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN u.Reputation > 1000 THEN p.Id ELSE NULL END) AS REAL) * 100 / COUNT(p.Id) FROM posts AS p INNER JOIN users AS u ON p.OwnerUserId = u.Id WHERE STRFTIME('%Y', p.CreaionDate) = '2011'
SELECT CAST(COUNT(CASE WHEN Age BETWEEN 13 AND 18 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(Id) AS percentage FROM users
SELECT T1.ViewCount, T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Title = 'Computer game datasets'
SELECT COUNT(ViewCount) FROM posts WHERE ViewCount > ( SELECT AVG(ViewCount) FROM posts )
SELECT COUNT(*) FROM comments WHERE PostId IN (SELECT Id FROM posts ORDER BY Score DESC LIMIT 1)
SELECT COUNT(*) FROM posts WHERE ViewCount > 35000 AND CommentCount = 0
SELECT T3.DisplayName, T3.Location FROM postHistory AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id INNER JOIN users AS T3 ON T1.UserId = T3.Id WHERE T2.Id = 183 ORDER BY T1.CreationDate DESC LIMIT 1
SELECT T1.Name FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Emmett' ORDER BY T1.Date DESC LIMIT 1
SELECT COUNT(Id) FROM users WHERE Age BETWEEN 19 AND 65 AND UpVotes > 5000
SELECT (strftime('%J', T2.Date) - strftime('%J', T1.CreationDate)) AS days_diff FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'Zolomon'
SELECT COUNT(T2.Id) AS NumberOfPosts, COUNT(T3.Id) AS NumberOfComments  FROM users AS T1  JOIN posts AS T2 ON T1.Id = T2.OwnerUserId  JOIN comments AS T3 ON T1.Id = T3.UserId  WHERE T1.CreationDate = (SELECT MAX(CreationDate) FROM users)
SELECT T1.Text, T1.UserDisplayName FROM comments AS T1 JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T2.Title = 'Analysing wind data with R' ORDER BY T1.CreationDate DESC LIMIT 10
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Citizen Patrol'
SELECT COUNT(T2.Id) FROM tags AS T1 INNER JOIN posts AS T2 ON T1.ExcerptPostId = T2.Id WHERE T1.TagName = 'careers'
SELECT Reputation, Views FROM users WHERE DisplayName = 'Jarrod Dixon'
SELECT (SELECT COUNT(*) FROM comments WHERE PostId IN (SELECT Id FROM posts WHERE Title = 'Clustering 1D data')) + (SELECT COUNT(*) FROM posts WHERE Title = 'Clustering 1D data' AND ParentId <> 0 AND PostTypeId = 2) AS Total_Items
SELECT CreationDate FROM users WHERE DisplayName = 'IrishStat'
SELECT COUNT(Id) FROM votes WHERE BountyAmount >= 30
SELECT CAST(COUNT(CASE WHEN T2.Score > 50 THEN T2.Id ELSE NULL END) AS REAL) * 100 / COUNT(T2.Id) FROM users AS T1 INNER JOIN posts AS T2 ON T1.Id = T2.OwnerUserId WHERE T1.Reputation = ( SELECT MAX(Reputation) FROM users )
SELECT COUNT(Id) FROM posts WHERE Score < 20
SELECT COUNT(Id) FROM tags WHERE Id < 15 AND Count <= 20
SELECT ExcerptPostId, WikiPostId FROM tags WHERE TagName = 'sample'
SELECT T2.Reputation, T2.UpVotes FROM comments AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Text = 'fine, you win :)'
SELECT c.Text FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE p.Title LIKE '%linear regression%'
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.ViewCount BETWEEN 100 AND 150 ORDER BY T2.Score DESC LIMIT 1
SELECT T2.CreationDate, T2.Age FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Text LIKE '%http://%'
SELECT COUNT(T1.Id) FROM posts AS T1 JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.ViewCount < 5 AND T2.Score = 0
SELECT COUNT(*) FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.CommentCount = 1 AND T2.Score = 0
SELECT COUNT(DISTINCT T2.Id) FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Score = 0 AND T2.Age = 40
SELECT T1.Id, T2.Text FROM posts AS T1 JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.Title = 'Group differences on a five point Likert item'
SELECT T2.UpVotes FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Text = 'R is also lazy evaluated.'
SELECT T1.Text FROM comments AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Harvey Motulsky'
SELECT T2.DisplayName FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Score BETWEEN 1 AND 5 AND T2.DownVotes = 0
SELECT CAST(SUM(CASE WHEN T2.UpVotes = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.Id) FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Score BETWEEN 5 AND 10
SELECT T3.power_name FROM hero_power AS T1 INNER JOIN superpower AS T3 ON T1.power_id = T3.id INNER JOIN superhero AS T2 ON T1.hero_id = T2.id WHERE T2.superhero_name = '3-D Man'
SELECT COUNT(*) FROM hero_power AS T1 JOIN superpower AS T2 ON T1.power_id = T2.id WHERE T2.power_name = 'Super Strength'
SELECT COUNT(*) FROM superpower AS T1 JOIN hero_power AS T2 ON T1.id = T2.power_id JOIN superhero AS T3 ON T2.hero_id = T3.id WHERE T1.power_name = 'Super Strength' AND T3.height_cm > 200
SELECT T1.full_name FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id GROUP BY T1.full_name HAVING COUNT(T2.power_id) > 15
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T2.colour = 'Blue'
SELECT T2.colour FROM colour AS T2 INNER JOIN superhero AS T1 ON T1.skin_colour_id = T2.id WHERE T1.superhero_name = 'Apocalypse'
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id INNER JOIN hero_power AS T3 ON T1.id = T3.hero_id INNER JOIN superpower AS T4 ON T3.power_id = T4.id WHERE T2.colour = 'Blue' AND T4.power_name = 'Agility'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id INNER JOIN colour AS T3 ON T1.hair_colour_id = T3.id WHERE T2.colour = 'Blue' AND T3.colour = 'Blond'
SELECT COUNT(*) FROM superhero AS T1 JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T2.publisher_name = 'Marvel Comics'
SELECT T1.superhero_name AS name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T2.publisher_name = 'Marvel Comics' ORDER BY T1.height_cm DESC
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.superhero_name = 'Sauron'
SELECT T3.colour FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id INNER JOIN colour AS T3 ON T1.eye_colour_id = T3.id INNER JOIN publisher AS T4 ON T1.publisher_id = T4.id WHERE T4.publisher_name = 'Marvel Comics' GROUP BY T3.colour ORDER BY COUNT(T1.id) DESC LIMIT 1
SELECT AVG(superhero.height_cm) FROM superhero JOIN publisher ON superhero.publisher_id = publisher.id WHERE publisher.publisher_name = 'Marvel Comics'
SELECT DISTINCT s.superhero_name FROM superhero s INNER JOIN hero_power hp ON s.id = hp.hero_id INNER JOIN superpower p ON hp.power_id = p.id INNER JOIN publisher pu ON s.publisher_id = pu.id WHERE pu.publisher_name = 'Marvel Comics' AND p.power_name = 'Super Strength'
SELECT COUNT(*) FROM superhero WHERE publisher_id IN (SELECT id FROM publisher WHERE publisher_name = 'DC Comics')
SELECT T1.publisher_name FROM publisher AS T1 JOIN superhero AS T2 ON T1.id = T2.publisher_id JOIN hero_attribute AS T3 ON T2.id = T3.hero_id JOIN attribute AS T4 ON T3.attribute_id = T4.id WHERE T4.attribute_name = 'Speed' ORDER BY T3.attribute_value ASC LIMIT 1
SELECT COUNT(*) FROM superhero AS T1  INNER JOIN colour AS T2  ON T1.eye_colour_id = T2.id  INNER JOIN publisher AS T3  ON T1.publisher_id = T3.id  WHERE T2.colour = 'Gold' AND T3.publisher_name = 'Marvel Comics'
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.superhero_name = 'Blue Beetle II'
SELECT COUNT(*) FROM superhero AS s JOIN colour AS c ON s.hair_colour_id = c.id WHERE c.colour = 'Blond'
SELECT T1.superhero_name FROM superhero AS T1 JOIN hero_attribute AS T2 ON T1.id = T2.hero_id JOIN attribute AS T3 ON T2.attribute_id = T3.id WHERE T3.attribute_name = 'Intelligence' ORDER BY T2.attribute_value ASC LIMIT 1
SELECT T1.race FROM race AS T1 INNER JOIN superhero AS T2 ON T1.id = T2.race_id WHERE T2.superhero_name = 'Copycat'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN hero_attribute AS T2 ON T1.id = T2.hero_id INNER JOIN attribute AS T3 ON T2.attribute_id = T3.id WHERE T3.attribute_name = 'Durability' AND T2.attribute_value < 50
SELECT T3.superhero_name FROM hero_power AS T1 INNER JOIN superpower AS T2 ON T1.power_id = T2.id INNER JOIN superhero AS T3 ON T1.hero_id = T3.id WHERE T2.power_name = 'Death Touch'
SELECT COUNT(*) FROM superhero AS S INNER JOIN gender AS G ON S.gender_id = G.id INNER JOIN hero_attribute AS H_A ON S.id = H_A.hero_id INNER JOIN attribute AS A ON H_A.attribute_id = A.id WHERE G.gender = 'Female' AND A.attribute_name = 'Strength' AND H_A.attribute_value = 100
SELECT T2.superhero_name FROM hero_power AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id GROUP BY T2.superhero_name ORDER BY COUNT(T1.power_id) DESC LIMIT 1
SELECT COUNT(*) FROM superhero AS T1 JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Vampire'
SELECT CAST(SUM(CASE WHEN T1.alignment = 'Bad' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id), COUNT(CASE WHEN T1.alignment = 'Bad' AND T3.publisher_name = 'Marvel Comics' THEN 1 ELSE NULL END) FROM alignment AS T1 JOIN superhero AS T2 ON T1.id = T2.alignment_id JOIN publisher AS T3 ON T2.publisher_id = T3.id
SELECT (SUM(CASE WHEN T2.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.publisher_name = 'DC Comics' THEN 1 ELSE 0 END)) AS difference FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id
SELECT id FROM publisher WHERE publisher_name = 'Star Trek'
SELECT AVG(attribute_value) FROM hero_attribute
SELECT COUNT(*) FROM superhero WHERE full_name IS NULL
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.id = 75
SELECT T2.power_name FROM hero_power AS T1 INNER JOIN superpower AS T2 ON T1.power_id = T2.id INNER JOIN superhero AS T3 ON T1.hero_id = T3.id WHERE T3.superhero_name = 'Deathlok'
SELECT AVG(T1.weight_kg) FROM superhero AS T1 JOIN gender AS T2 ON T1.gender_id = T2.id WHERE T2.gender = 'Female'
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id JOIN gender AS T4 ON T1.gender_id = T4.id WHERE T4.gender = 'Male' LIMIT 5
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Alien'
SELECT T1.superhero_name FROM superhero AS T1 JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.height_cm BETWEEN 170 AND 190 AND T2.colour = 'No Colour'
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T1.id = 56
SELECT T1.full_name FROM superhero AS T1 JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Demi-God' LIMIT 5
SELECT COUNT(superhero_name) FROM superhero AS T2 INNER JOIN alignment AS T1 ON T2.alignment_id = T1.id WHERE T1.alignment = 'Bad'
SELECT T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.weight_kg = 169
SELECT T1.colour FROM colour AS T1 JOIN superhero AS T2 ON T1.id = T2.hair_colour_id WHERE T2.height_cm = 185 AND T2.race_id = (SELECT id FROM race WHERE race = 'Human')
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id ORDER BY T1.weight_kg DESC LIMIT 1
SELECT CAST(SUM(CASE WHEN T2.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.height_cm BETWEEN 150 AND 180
SELECT T1.superhero_name FROM superhero AS T1 WHERE T1.gender_id = (SELECT id FROM gender WHERE gender = 'Male') AND T1.weight_kg > ( SELECT AVG(weight_kg) FROM superhero ) * 0.79
SELECT sp.power_name FROM superhero AS s JOIN hero_power AS hp ON s.id = hp.hero_id JOIN superpower AS sp ON hp.power_id = sp.id GROUP BY sp.power_name ORDER BY COUNT(sp.power_name) DESC LIMIT 1
SELECT T1.attribute_value FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id WHERE T2.superhero_name = 'Abomination'
SELECT T2.power_name FROM hero_power AS T1 INNER JOIN superpower AS T2 ON T1.power_id = T2.id WHERE T1.hero_id = 1
SELECT COUNT(T2.hero_id) FROM superpower AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.power_id WHERE T1.power_name = 'Stealth'
SELECT T3.full_name FROM hero_attribute AS T1 INNER JOIN attribute AS T2 ON T1.attribute_id = T2.id INNER JOIN superhero AS T3 ON T1.hero_id = T3.id WHERE T2.attribute_name = 'Strength' ORDER BY T1.attribute_value DESC LIMIT 1
SELECT CAST( SUM(CASE WHEN superhero.skin_colour_id = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(superhero.id) FROM superhero
SELECT COUNT(T2.id) FROM publisher AS T1 INNER JOIN superhero AS T2 ON T1.id = T2.publisher_id WHERE T1.publisher_name = 'Dark Horse Comics'
SELECT T1.superhero_name FROM superhero AS T1 JOIN hero_attribute AS T2 ON T1.id = T2.hero_id JOIN attribute AS T3 ON T2.attribute_id = T3.id JOIN publisher AS T4 ON T1.publisher_id = T4.id WHERE T4.publisher_name = 'Dark Horse Comics' AND T3.attribute_name = 'Durability' ORDER BY T2.attribute_value DESC LIMIT 1
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.full_name = 'Abraham Sapien'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id INNER JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T3.power_name = 'Flight'
SELECT T2.colour AS eye_colour, T3.colour AS hair_colour, T4.colour AS skin_colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id INNER JOIN colour AS T3 ON T1.hair_colour_id = T3.id INNER JOIN colour AS T4 ON T1.skin_colour_id = T4.id INNER JOIN publisher AS T5 ON T1.publisher_id = T5.id WHERE T1.gender_id = (SELECT id FROM gender WHERE gender = 'Female') AND T5.publisher_name = 'Dark Horse Comics'
SELECT T1.superhero_name, T2.publisher_name FROM superhero AS T1 JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.hair_colour_id = T1.skin_colour_id AND T1.hair_colour_id = T1.eye_colour_id
SELECT T2.race FROM superhero AS T1 JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.superhero_name = 'A-Bomb'
SELECT (CAST(SUM(CASE WHEN T3.colour = 'Blue' THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(*) FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id INNER JOIN colour AS T3 ON T1.skin_colour_id = T3.id WHERE T2.gender = 'Female'
SELECT T1.superhero_name, T3.race FROM superhero AS T1 JOIN race AS T3 ON T1.race_id = T3.id WHERE T1.full_name = 'Charles Chandler'
SELECT T2.gender FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id WHERE T1.superhero_name = 'Agent 13'
SELECT T3.superhero_name FROM hero_power AS T1 JOIN superpower AS T2 ON T1.power_id = T2.id JOIN superhero AS T3 ON T1.hero_id = T3.id WHERE T2.power_name = 'Adaptation'
SELECT COUNT(T2.power_id) FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id WHERE T1.superhero_name = 'Amazo'
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T1.full_name = 'Hunter Zolomon'
SELECT T1.height_cm FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T2.colour = 'Amber'
SELECT superhero_name FROM superhero AS superhero JOIN colour AS colour ON superhero.eye_colour_id = colour.id AND superhero.hair_colour_id = colour.id WHERE colour.colour = 'Black'
SELECT T1.colour FROM colour AS T1 INNER JOIN superhero AS T2 ON T2.skin_colour_id = T1.id WHERE T1.colour = 'Gold'
SELECT T1.full_name FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Vampire'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id WHERE T2.alignment = 'Neutral'
SELECT COUNT(*) FROM hero_attribute AS ha INNER JOIN attribute AS a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Strength' AND ha.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute WHERE attribute_id = ( SELECT id FROM attribute WHERE attribute_name = 'Strength' ) )
SELECT T2.race, T3.alignment FROM superhero AS T1 JOIN race AS T2 ON T1.race_id = T2.id JOIN alignment AS T3 ON T1.alignment_id = T3.id WHERE T1.superhero_name = 'Cameron Hicks'
SELECT CAST(SUM(CASE WHEN T1.gender = 'Female' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM gender AS T1 JOIN superhero AS T2 ON T1.id = T2.gender_id JOIN publisher AS T3 ON T2.publisher_id = T3.id WHERE T3.publisher_name = 'Marvel Comics'
SELECT AVG(t1.weight_kg) FROM superhero AS t1 JOIN race AS t2 ON t1.race_id = t2.id WHERE t2.race = 'Alien'
SELECT SUM(CASE WHEN full_name = 'Emil Blonsky' THEN weight_kg ELSE 0 END) - SUM(CASE WHEN full_name = 'Charles Chandler' THEN weight_kg ELSE 0 END) AS weight_difference FROM superhero
SELECT AVG(height_cm) FROM superhero
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T1.superhero_name = 'Abomination'
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id WHERE T1.race_id = 21 AND T2.gender = 'Male'
SELECT T3.superhero_name FROM hero_attribute AS T1 JOIN attribute AS T2 ON T1.attribute_id = T2.id JOIN superhero AS T3 ON T1.hero_id = T3.id WHERE T2.attribute_name = 'Speed' ORDER BY T1.attribute_value DESC LIMIT 1
SELECT COUNT(id) FROM superhero WHERE alignment_id = 3
SELECT attribute.attribute_name, hero_attribute.attribute_value FROM superhero AS superhero INNER JOIN hero_attribute AS hero_attribute ON superhero.id = hero_attribute.hero_id INNER JOIN attribute AS attribute ON hero_attribute.attribute_id = attribute.id WHERE superhero_name = '3-D Man'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id INNER JOIN colour AS T3 ON T1.hair_colour_id = T3.id WHERE T2.colour = 'Blue' AND T3.colour = 'Brown'
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.superhero_name IN ('Hawkman', 'Karate Kid', 'Speedy')
SELECT COUNT(*) FROM superhero WHERE publisher_id = 1
SELECT CAST(COUNT(CASE WHEN T2.colour = 'Blue' THEN 1 ELSE NULL END) AS REAL) * 100.0 / COUNT(*) FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id
SELECT CAST(SUM(CASE WHEN T1.gender_id = 1 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN T1.gender_id = 2 THEN 1 ELSE 0 END) AS ratio FROM superhero AS T1
SELECT superhero_name FROM superhero ORDER BY height_cm DESC LIMIT 1
SELECT id FROM superpower WHERE power_name = 'Cryokinesis'
SELECT superhero_name FROM superhero WHERE id = 294
SELECT full_name FROM superhero WHERE weight_kg = 0 OR weight_kg IS NULL
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.full_name = 'Karen Beecher-Duncan'
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T3.id = T2.power_id WHERE T1.full_name = 'Helen Parr'
SELECT T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.weight_kg = 108 AND T1.height_cm = 188
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.id = 38
SELECT T3.race FROM superhero AS T1 JOIN hero_attribute AS T2 ON T1.id = T2.hero_id JOIN race AS T3 ON T1.race_id = T3.id WHERE T2.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute ) LIMIT 1
SELECT T2.alignment, T4.power_name FROM superhero AS T1 JOIN alignment AS T2 ON T1.alignment_id = T2.id JOIN hero_power AS T3 ON T1.id = T3.hero_id JOIN superpower AS T4 ON T3.power_id = T4.id WHERE T1.superhero_name = 'Atom IV'
SELECT t1.full_name FROM superhero AS t1 INNER JOIN colour AS t2 ON t1.eye_colour_id = t2.id WHERE t2.colour = 'Blue' LIMIT 5
SELECT AVG(T2.attribute_value) FROM superhero AS T1 INNER JOIN hero_attribute AS T2 ON T1.id = T2.hero_id WHERE T1.alignment_id = 3
SELECT T3.colour FROM hero_attribute AS T1 JOIN superhero AS T2 ON T1.hero_id = T2.id JOIN colour AS T3 ON T2.skin_colour_id = T3.id WHERE T1.attribute_value = 100
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id INNER JOIN alignment AS T3 ON T1.alignment_id = T3.id WHERE T2.gender = 'Female' AND T3.alignment = 'Good'
SELECT T2.superhero_name FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id WHERE T1.attribute_value BETWEEN 75 AND 80
SELECT T3.race FROM superhero AS T1 JOIN colour AS T2 ON T1.hair_colour_id = T2.id JOIN gender AS T4 ON T1.gender_id = T4.id JOIN race AS T3 ON T1.race_id = T3.id WHERE T2.colour = 'Blue' AND T4.gender = 'Male'
SELECT CAST(COUNT(CASE WHEN T2.gender = 'Female' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(T3.alignment_id) FROM gender AS T2 JOIN superhero AS T3 ON T2.id = T3.gender_id JOIN alignment AS T4 ON T3.alignment_id = T4.id WHERE T4.alignment = 'Bad'
SELECT SUM(CASE WHEN T2.id = 7 THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.id = 1 THEN 1 ELSE 0 END) AS difference FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.weight_kg = 0 OR T1.weight_kg IS NULL
SELECT T2.attribute_value FROM superhero AS T1 JOIN hero_attribute AS T2 ON T1.id = T2.hero_id JOIN attribute AS T3 ON T2.attribute_id = T3.id WHERE T1.superhero_name = 'Hulk' AND T3.attribute_name = 'Strength'
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T1.superhero_name = 'Ajax'
SELECT COUNT(*) FROM alignment AS T1  JOIN superhero AS T2 ON T1.id = T2.alignment_id  JOIN colour AS T3 ON T2.skin_colour_id = T3.id  WHERE T3.colour = 'Green' AND T1.alignment = 'Bad'
SELECT COUNT(*) FROM superhero AS s JOIN publisher AS p ON s.publisher_id = p.id WHERE s.gender_id = (SELECT id FROM gender WHERE gender = 'Female') AND p.publisher_name = 'Marvel Comics'
SELECT T1.superhero_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T3.power_name = 'Wind Control' ORDER BY T1.superhero_name
SELECT T1.gender FROM gender AS T1 JOIN superhero AS T2 ON T1.id = T2.gender_id JOIN hero_power AS T3 ON T2.id = T3.hero_id JOIN superpower AS T4 ON T3.power_id = T4.id WHERE T4.power_name = 'Phoenix Force'
SELECT T1.superhero_name FROM superhero AS T1 JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T2.publisher_name = 'DC Comics' ORDER BY T1.weight_kg DESC LIMIT 1
SELECT AVG(T1.height_cm) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id INNER JOIN race AS T3 ON T1.race_id = T3.id WHERE T3.race <> 'Human' AND T2.publisher_name = 'Dark Horse Comics'
SELECT COUNT(*) FROM superhero AS s INNER JOIN hero_attribute AS ha ON s.id = ha.hero_id INNER JOIN attribute AS a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Speed' AND ha.attribute_value = 100
SELECT SUM(CASE WHEN T1.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T1.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS difference FROM publisher AS T1 JOIN superhero AS T2 ON T1.id = T2.publisher_id
SELECT DISTINCT T1.attribute_name FROM attribute AS T1 INNER JOIN hero_attribute AS T2 ON T1.id = T2.attribute_id INNER JOIN superhero AS T3 ON T2.hero_id = T3.id WHERE T3.superhero_name = 'Black Panther' ORDER BY T2.attribute_value ASC LIMIT 1
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.superhero_name = 'Abomination'
SELECT superhero_name FROM superhero ORDER BY height_cm DESC LIMIT 1
SELECT superhero_name FROM superhero WHERE full_name = 'Charles Chandler'
SELECT CAST(SUM(CASE WHEN T3.gender = 'Female' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id INNER JOIN gender AS T3 ON T1.gender_id = T3.id WHERE T2.publisher_name = 'George Lucas'
SELECT CAST(SUM(CASE WHEN T3.alignment = 'Good' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id INNER JOIN alignment AS T3 ON T1.alignment_id = T3.id WHERE T2.publisher_name = 'Marvel Comics'
SELECT COUNT(*) FROM superhero WHERE full_name LIKE 'John%'
SELECT hero_id FROM hero_attribute WHERE attribute_value = ( SELECT MIN(attribute_value) FROM hero_attribute )
SELECT full_name FROM superhero WHERE superhero_name = 'Alien'
SELECT T1.full_name FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.weight_kg < 100 AND T2.colour = 'Brown'
SELECT T2.attribute_value  FROM superhero AS T1  JOIN hero_attribute AS T2  ON T1.id = T2.hero_id  WHERE T1.superhero_name = 'Aquababy'
SELECT T1.weight_kg, T2.race FROM superhero AS T1 JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.id = 40
SELECT AVG(T1.height_cm) FROM superhero AS T1 JOIN alignment AS T2 ON T1.alignment_id = T2.id WHERE T2.alignment = 'Neutral'
SELECT h.hero_id FROM hero_power AS h INNER JOIN superpower AS s ON h.power_id = s.id WHERE s.power_name = 'Intelligence'
SELECT T1.colour FROM colour AS T1 INNER JOIN superhero AS T2 ON T1.id = T2.eye_colour_id WHERE T2.superhero_name = 'Blackwulf'
SELECT T2.power_name FROM superhero AS T1 JOIN hero_power AS T3 ON T1.id = T3.hero_id JOIN superpower AS T2 ON T3.power_id = T2.id WHERE T1.height_cm > ( SELECT AVG(height_cm) * 0.8 FROM superhero )
SELECT DISTINCT T2.driverRef  FROM qualifying AS T1  JOIN drivers AS T2  ON T1.driverId = T2.driverId  WHERE T1.raceId = 20  ORDER BY T1.q1 DESC  LIMIT 5
SELECT T2.surname FROM qualifying AS T1 JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 19 AND T1.position = 2 ORDER BY T1.q2 ASC LIMIT 1
SELECT DISTINCT T2.year FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.location = 'Shanghai'
SELECT T1.url FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T2.name = 'Circuit de Barcelona-Catalunya'
SELECT T1.name FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T2.country = 'Germany'
SELECT position FROM constructorStandings WHERE constructorId IN (SELECT constructorId FROM constructors WHERE name = 'Renault')
SELECT COUNT(*) FROM races AS T1 INNER JOIN circuits AS T3 ON T1.circuitId = T3.circuitId WHERE T1.year = 2010 AND T3.location NOT LIKE '%Asia%' AND T3.location NOT LIKE '%Europe%'
SELECT T2.name FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.country = 'Spain'
SELECT T2.lat, T2.lng FROM races AS T1 JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Australian Grand Prix'
SELECT T2.url FROM circuits AS T1 JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Sepang International Circuit'
SELECT T1.time FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T2.name = 'Sepang International Circuit'
SELECT T2.lat, T2.lng FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Abu Dhabi Grand Prix'
SELECT T1.country FROM circuits AS T1 JOIN races AS T2 ON T1.circuitId = T2.circuitId JOIN constructorResults AS T3 ON T3.raceId = T2.raceId JOIN constructors AS T4 ON T4.constructorId = T3.constructorId WHERE T2.raceId = 24 AND T3.points = 1
SELECT T1.q1 FROM qualifying AS T1 JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T2.forename = 'Bruno' AND T2.surname = 'Senna' AND T1.raceId = 354
SELECT T2.nationality FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.q2 = '0:01:40' AND T1.raceId = 355 LIMIT 1
SELECT T2.number FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 903 AND T1.q3 LIKE '0:01:54%'
SELECT COUNT(*) FROM races AS T1 JOIN results AS T2 ON T1.raceid = T2.raceid WHERE T1.name = 'Bahrain Grand Prix' AND T1.year = 2007 AND T2.time IS NULL
SELECT T2.url FROM races AS T1 INNER JOIN seasons AS T2 ON T1.year = T2.year WHERE T1.raceId = 901
SELECT COUNT(DISTINCT driverId) FROM results WHERE raceId IN (SELECT raceId FROM races WHERE date = '2015-11-29')
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId = 592 AND T2.time IS NOT NULL ORDER BY T1.dob ASC LIMIT 1
SELECT T1.url FROM drivers AS T1 JOIN lapTimes AS T2 ON T1.driverId = T2.driverId WHERE T2.lap = 1 AND T2.raceId = 161
SELECT T2.nationality FROM results AS T1 JOIN drivers AS T2 ON T1.driverId = T2.driverId JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T3.raceId = 933 ORDER BY T1.fastestLapSpeed DESC LIMIT 1
SELECT T2.lat, T2.lng FROM races AS T1 JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Malaysian Grand Prix'
SELECT url FROM constructors WHERE constructorId IN ( SELECT constructorId FROM constructorResults WHERE raceId = 9 ORDER BY points DESC LIMIT 1 )
SELECT T2.q1 FROM drivers AS T1 INNER JOIN qualifying AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.forename = 'Lucas' AND T1.surname = 'di Grassi' AND T3.raceId = 345
SELECT T2.nationality FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 347 AND T1.q2 = '0:01:15'
SELECT T1.code FROM drivers AS T1 JOIN qualifying AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId = 45 AND T2.q3 = '0:01:33'
SELECT DISTINCT results.time FROM drivers AS drivers INNER JOIN results AS results ON drivers.driverId = results.driverId INNER JOIN races AS races ON results.raceId = races.raceId WHERE drivers.forename = 'Bruce' AND drivers.surname = 'McLaren' AND races.raceId = 743
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T3.raceId = T2.raceId WHERE T3.year = 2006 AND T3.name = 'San Marino Grand Prix' AND T2.position = 2
SELECT T2.url FROM races AS T1 INNER JOIN seasons AS T2 ON T1.year = T2.year WHERE T1.raceId = 901
SELECT COUNT(DISTINCT T2.driverId) FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId WHERE T1.date = '2015-11-29' AND T2.time IS NULL
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId = 872 ORDER BY T1.dob DESC LIMIT 1
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN laptimes AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId = 348 ORDER BY T2.time ASC LIMIT 1
SELECT T1.nationality FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
SELECT (CAST((SELECT fastestLapSpeed FROM results WHERE driverId = (SELECT driverId FROM drivers WHERE forename = 'Paul' AND surname = 'di Resta') AND raceId = 853) - (SELECT fastestLapSpeed FROM results WHERE driverId = (SELECT driverId FROM drivers WHERE forename = 'Paul' AND surname = 'di Resta') AND raceId = 854) AS REAL) * 100) / (SELECT fastestLapSpeed FROM results WHERE driverId = (SELECT driverId FROM drivers WHERE forename = 'Paul' AND surname = 'di Resta') AND raceId = 854) FROM driver
SELECT CAST(SUM(CASE WHEN T2.milliseconds IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.driverId) FROM drivers AS T1 LEFT JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId IN (SELECT raceId FROM races WHERE `date` = '1983-07-16')
SELECT year FROM races WHERE name = 'Singapore Grand Prix' ORDER BY year ASC LIMIT 1
SELECT COUNT(*) FROM races WHERE year = 2005
SELECT name FROM races WHERE date IN (SELECT MIN(date) FROM races)
SELECT name, date FROM races WHERE year = 1999 ORDER BY round DESC LIMIT 1
SELECT YEAR FROM races GROUP BY YEAR ORDER BY COUNT(*) DESC LIMIT 1
SELECT name FROM races WHERE YEAR = 2017 AND raceId NOT IN (SELECT raceId FROM races WHERE YEAR = 2000)
SELECT T2.country, T2.name, T2.location FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'European Grand Prix' ORDER BY T1.year ASC LIMIT 1
SELECT T1.year FROM races AS T1 JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T2.name = 'Brands Hatch' AND T1.name = 'British Grand Prix' ORDER BY T1.year DESC LIMIT 1
SELECT COUNT(DISTINCT T2.year) FROM circuits AS T1 JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T2.name = 'British Grand Prix' AND T1.name = 'Silverstone Circuit'
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T2.raceId IN (SELECT raceId FROM races WHERE `year` = 2010 AND name = 'Singapore Grand Prix') ORDER BY T2.position
SELECT T1.forename, T1.surname, T2.points FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.points DESC LIMIT 1
SELECT T2.forename, T2.surname, T1.points FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T3.year = 2017 AND T3.name = 'Chinese Grand Prix' ORDER BY T1.points DESC LIMIT 3
SELECT T2.milliseconds, T1.forename, T1.surname, T4.name FROM drivers AS T1 INNER JOIN lapTimes AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T4 ON T2.raceId = T4.raceId ORDER BY T2.milliseconds ASC LIMIT 1
SELECT AVG(laptimes.milliseconds) FROM drivers INNER JOIN results ON drivers.driverId = results.driverId INNER JOIN races ON results.raceId = races.raceId INNER JOIN laptimes ON results.raceId = laptimes.raceId AND results.driverId = laptimes.driverId WHERE drivers.forename = 'Lewis' AND drivers.surname = 'Hamilton' AND races.year = 2009 AND races.name = 'Malaysian Grand Prix'
SELECT CAST(SUM(CASE WHEN T2.position > 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM drivers AS T1 INNER JOIN driverStandings AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.surname = 'Hamilton' AND T3.year >= 2010
SELECT T2.forename, T2.surname, T2.nationality, T1.points FROM driverStandings AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId ORDER BY T1.wins DESC, T1.points DESC LIMIT 1
SELECT (STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', dob)) AS age, forename, surname FROM drivers WHERE nationality = 'Japanese' ORDER BY age ASC LIMIT 1
SELECT T1.name FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE STRFTIME('%Y', T2.date) BETWEEN '1990' AND '2000' GROUP BY T1.name HAVING COUNT(T2.raceId) = 4
SELECT T2.name, T2.location, T1.name FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.country = 'USA' AND T1.year = 2006
SELECT T1.name, T2.name, T2.location FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE strftime('%m', T1.date) = '09' AND strftime('%Y', T1.date) = '2005'
SELECT T3.name FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.forename = 'Alex' AND T1.surname = 'Yoong' AND T2.position < 20
SELECT SUM(CASE WHEN T2.`position` = 1 THEN 1 ELSE 0 END) AS num_wins FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId INNER JOIN circuits AS T4 ON T3.circuitId = T4.circuitId WHERE T1.forename = 'Michael' AND T1.surname = 'Schumacher' AND T4.name = 'Sepang International Circuit'
SELECT T1.name, T1.year FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T3.forename = 'Michael' AND T3.surname = 'Schumacher' ORDER BY T2.milliseconds ASC LIMIT 1
SELECT AVG(T1.points) FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T3.forename = 'Eddie' AND T3.surname = 'Irvine' AND T2.year = 2000
SELECT T2.name, T1.points FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T2.year ASC, T2.date ASC LIMIT 1
SELECT T1.name, T2.country FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T1.year = 2017 ORDER BY T1.date
SELECT T1.name, T1.year, T3.location FROM races AS T1 JOIN results AS T2 ON T1.raceId = T2.raceId JOIN circuits AS T3 ON T1.circuitId = T3.circuitId ORDER BY T2.laps DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN T2.country = 'Germany' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'European Grand Prix'
SELECT lat, lng FROM circuits WHERE name = 'Silverstone Circuit'
SELECT name FROM circuits WHERE circuitRef IN ('silverstone', 'hockenheimring', 'hungaroring') ORDER BY lat DESC LIMIT 1
SELECT circuitRef FROM circuits WHERE name = 'Marina Bay Street Circuit'
SELECT country FROM circuits ORDER BY alt DESC LIMIT 1
SELECT COUNT(*) FROM drivers WHERE code IS NULL
SELECT nationality FROM drivers ORDER BY dob ASC LIMIT 1
SELECT surname FROM drivers WHERE nationality = 'Italian'
SELECT url FROM drivers WHERE forename = 'Anthony' AND surname = 'Davidson'
SELECT driverRef FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton'
SELECT T2.name FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.year = 2009 AND T1.name = 'Spanish Grand Prix'
SELECT DISTINCT T1.year FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T2.name = 'Silverstone Circuit'
SELECT T2.url FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Silverstone Circuit'
SELECT T1.time FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.year = 2010 AND T2.location = 'Abu Dhabi'
SELECT COUNT(T2.raceId) FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.country = 'Italy'
SELECT T2.`date` FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitId = T2.circuitId WHERE T1.name = 'Sepang International Circuit'
SELECT T2.url FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitId = T2.circuitId WHERE T1.year = 2009 AND T1.name = 'Spanish Grand Prix'
SELECT MIN(T2.fastestLapTime) FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
SELECT T3.driverRef FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T2.name = 'Canadian Grand Prix' AND T2.year = 2007 AND T1.position = 1
SELECT T3.name FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T2.surname = 'Hamilton' AND T2.forename = 'Lewis'
SELECT T2.name FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T1.rank ASC LIMIT 1
SELECT T1.fastestLapSpeed FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.year = 2009 AND T2.name = 'Spanish Grand Prix' ORDER BY T1.fastestLapSpeed DESC LIMIT 1
SELECT DISTINCT T3.year FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
SELECT T2.positionOrder FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton' AND T2.raceId IN (SELECT raceId FROM races WHERE `year` = 2008 AND name = 'Chinese Grand Prix')
SELECT T3.forename, T3.surname FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T2.year = 1989 AND T1.grid = 4 AND T2.name = 'Australian Grand Prix'
SELECT COUNT(DISTINCT results.driverId) FROM results AS results INNER JOIN races AS races ON results.raceId = races.raceId WHERE races.year = 2008 AND races.name = 'Australian Grand Prix' AND results.time IS NOT NULL
SELECT T2.fastestLapTime FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.surname = 'Hamilton' AND T1.forename = 'Lewis' AND T3.year = 2008 AND T3.name = 'Australian Grand Prix'
SELECT T1.time FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.name = 'Australian Grand Prix' AND T1.rank = 2 AND T2.year = 2008
SELECT T3.forename, T3.surname, T3.url FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T2.year = 2008 AND T2.name = 'Australian Grand Prix' AND T1.position = 1
SELECT COUNT(DR.driverId) FROM drivers DR INNER JOIN results RS ON DR.driverId = RS.driverId INNER JOIN races RC ON RS.raceId = RC.raceId WHERE DR.nationality = 'British' AND RC.`year` = 2008 AND RC.name = 'Australian Grand Prix'
SELECT COUNT(DISTINCT T1.driverId) FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T3.`year` = 2008 AND T3.name = 'Chinese Grand Prix' AND T2.time IS NOT NULL
SELECT SUM(T2.points) FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
SELECT AVG(T1.fastestLapTime) AS average_fastest_lap_time_seconds FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T2.forename = 'Lewis' AND T2.surname = 'Hamilton'
SELECT CAST(SUM(CASE WHEN T1.time IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.raceId) FROM results AS T1 INNER JOIN races AS T2 ON T2.raceId = T1.raceId WHERE T2.year = 2008 AND T2.name = 'Australian Grand Prix'
SELECT (CAST((SUM(CASE WHEN rank = 50 THEN milliseconds ELSE 0 END) - SUM(CASE WHEN rank = 1 THEN milliseconds ELSE 0 END)) AS REAL) * 100) / SUM(CASE WHEN rank = 1 THEN milliseconds ELSE 0 END) FROM results WHERE raceId IN (SELECT raceId FROM races WHERE year = 2008 AND name = 'Australian Grand Prix')
SELECT COUNT(*) FROM circuits WHERE country = 'Australia' AND location = 'Adelaide'
SELECT lat, lng FROM circuits WHERE country = 'USA'
SELECT COUNT(*) FROM drivers WHERE nationality = 'British' AND STRFTIME('%Y', dob) > '1980'
SELECT MAX(T2.points) FROM constructors AS T1 INNER JOIN constructorResults AS T2 ON T1.constructorId = T2.constructorId WHERE T1.nationality = 'British'
SELECT T1.name FROM constructors AS T1 JOIN constructorStandings AS T2 ON T1.constructorId = T2.constructorId ORDER BY T2.points DESC LIMIT 1
SELECT T2.name FROM constructorResults AS T1 INNER JOIN constructors AS T2 ON T1.constructorId = T2.constructorId WHERE T1.raceId = 291 AND T1.points = 0
SELECT COUNT(T1.constructorId) FROM constructorStandings AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T1.points = 0 AND T1.constructorId IN (SELECT constructorId FROM constructors WHERE nationality = 'Japanese') GROUP BY T1.constructorId HAVING COUNT(T2.raceId) = 2
SELECT DISTINCT T2.name FROM results AS T1 INNER JOIN constructors AS T2 ON T1.constructorId = T2.constructorId WHERE T1.rank = 1
SELECT COUNT(T2.constructorId) FROM results AS T1 INNER JOIN constructors AS T2 ON T1.constructorId = T2.constructorId WHERE T1.laps > 50 AND T2.nationality = 'French'
SELECT (CAST(SUM(CASE WHEN T2.time IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(T2.driverId) FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.nationality = 'Japanese' AND T3.year BETWEEN 2007 AND 2009
SELECT AVG((strftime('%M', T1.time) * 60) + strftime('%S', T1.time) + (strftime('%f', T1.time) / 1000)) FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T1.statusId = 1 AND T2.year < 1975
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE strftime('%Y', T1.dob) > '1975' AND T2.rank = 2
SELECT COUNT(T1.driverId) FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'Italian' AND T2.time IS NULL
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN lapTimes AS T2 ON T1.driverId = T2.driverId ORDER BY T2.time ASC LIMIT 1
SELECT T2.fastestLap FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T1.year = 2009 ORDER BY T2.points DESC LIMIT 1
SELECT AVG(T2.fastestLapSpeed) FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId WHERE T1.year = 2009 AND T1.name = 'Spanish Grand Prix'
SELECT T1.name, T1.year FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId WHERE T2.milliseconds IS NOT NULL ORDER BY T2.milliseconds ASC LIMIT 1
SELECT CAST(SUM(CASE WHEN T1.laps > 50 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T3.year BETWEEN 2000 AND 2005 AND (strftime('%Y', T2.dob) < '1985') OR (strftime('%Y', T2.dob) BETWEEN '2000' AND '2005')
SELECT COUNT(*) FROM drivers AS T1 JOIN lapTimes AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'French' AND T2.milliseconds < 120000
SELECT code FROM drivers WHERE nationality = 'American'
SELECT raceId FROM races WHERE year = 2009
SELECT COUNT(DISTINCT driverId) FROM results WHERE raceId = 18
SELECT COUNT(CASE WHEN nationality = 'Dutch' THEN 1 END) AS Dutch_Drivers FROM drivers ORDER BY (strftime('%Y', 'now') - strftime('%Y', dob)) ASC LIMIT 3
SELECT driverRef FROM drivers WHERE forename = 'Robert' AND surname = 'Kubica'
SELECT COUNT(driverId) FROM drivers WHERE nationality = 'British' AND STRFTIME('%Y', dob) = '1980'
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN laptimes AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'German' AND strftime('%Y', T1.dob) BETWEEN '1980' AND '1990' ORDER BY T2.time ASC LIMIT 3
SELECT driverRef FROM drivers WHERE nationality = 'German' ORDER BY dob ASC LIMIT 1
SELECT DISTINCT D.driverId, D.code FROM drivers D INNER JOIN results R ON D.driverId = R.driverId WHERE STRFTIME('%Y', D.dob) = '1971' AND R.fastestLapTime IS NOT NULL
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN laptimes AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'Spanish' AND STRFTIME('%Y', T1.dob) < '1982' ORDER BY T2.time DESC LIMIT 10
SELECT T2.year FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId ORDER BY T1.fastestLapTime ASC LIMIT 1
SELECT T2.year FROM lapTimes AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId ORDER BY T1.time DESC LIMIT 1
SELECT driverId, time FROM lapTimes WHERE lap = 1 ORDER BY time ASC LIMIT 5
SELECT COUNT(*) FROM results WHERE statusId = 2 AND time IS NOT NULL AND raceId BETWEEN 50 AND 100
SELECT COUNT(circuitId), lat, lng FROM circuits WHERE country = 'Austria'
SELECT T2.raceId FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T1.time IS NOT NULL GROUP BY T2.raceId ORDER BY COUNT(T1.raceId) DESC LIMIT 1
SELECT T2.driverRef, T2.nationality, T2.dob FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 23 AND T1.q2 IS NOT NULL
SELECT T2.year, T2.name, T2.date, T2.time FROM drivers AS T1 JOIN qualifying AS T3 ON T1.driverId = T3.driverId JOIN races AS T2 ON T3.raceId = T2.raceId ORDER BY T1.dob DESC, T2.date ASC LIMIT 1
SELECT COUNT(T1.driverId) FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN status AS T3 ON T2.statusId = T3.statusId WHERE T1.nationality = 'American' AND T3.status = 'Puncture'
SELECT T1.url FROM constructors AS T1 INNER JOIN constructorStandings AS T2 ON T1.constructorId = T2.constructorId WHERE T1.nationality = 'Italian' ORDER BY T2.points DESC LIMIT 1
SELECT T1.url FROM constructors AS T1 JOIN constructorStandings AS T2 ON T1.constructorId = T2.constructorId GROUP BY T1.constructorId ORDER BY SUM(T2.wins) DESC LIMIT 1
SELECT T2.forename, T2.surname FROM races AS T1 JOIN lapTimes AS T3 ON T1.raceId = T3.raceId JOIN drivers AS T2 ON T3.driverId = T2.driverId WHERE T1.name = 'French Grand Prix' AND T3.lap = 3 ORDER BY T3.time DESC LIMIT 1
SELECT T2.name, T1.milliseconds FROM lapTimes AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T1.lap = 1 ORDER BY T1.milliseconds ASC LIMIT 1
SELECT AVG(T1.fastestLapTime) FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.year = 2006 AND T2.name = 'United States Grand Prix' AND T1.rank < 11
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN pitStops AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'German' AND STRFTIME('%Y', T1.dob) BETWEEN '1980' AND '1985' GROUP BY T1.driverId ORDER BY AVG(T2.duration) ASC LIMIT 3
SELECT T2.time FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T1.year = 2008 AND T1.name = 'Canadian Grand Prix' ORDER BY T2.points DESC LIMIT 1
SELECT T3.constructorRef, T3.url FROM results AS T1 INNER JOIN constructorResults AS T2 ON T1.constructorId = T2.constructorId INNER JOIN constructors AS T3 ON T3.constructorId = T2.constructorId INNER JOIN races AS T4 ON T4.raceId = T1.raceId WHERE T4.year = 2009 AND T4.name = 'Singapore Grand Prix' ORDER BY T1.time DESC LIMIT 1
SELECT forename, surname, dob FROM drivers WHERE nationality = 'Austrian' AND strftime('%Y', dob) BETWEEN '1981' AND '1991'
SELECT forename, surname, url, dob FROM drivers WHERE nationality = 'German' AND STRFTIME('%Y', dob) BETWEEN '1971' AND '1985' ORDER BY dob DESC
SELECT location, country, lat, lng FROM circuits WHERE name = 'Hungaroring'
SELECT T1.points, T3.name, T3.nationality FROM constructorResults AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN constructors AS T3 ON T1.constructorId = T3.constructorId WHERE T2.name = 'Monaco Grand Prix' AND T2.year BETWEEN 1980 AND 2010 ORDER BY T1.points DESC LIMIT 1
SELECT AVG(results.points) FROM drivers INNER JOIN results ON drivers.driverId = results.driverId INNER JOIN races ON results.raceId = races.raceId WHERE drivers.surname = 'Hamilton' AND races.name = 'Turkish Grand Prix'
SELECT CAST(COUNT(*) AS REAL) / 11 FROM races WHERE date BETWEEN '2000-01-01' AND '2010-12-31'
SELECT nationality FROM drivers GROUP BY nationality ORDER BY COUNT(nationality) DESC LIMIT 1
SELECT COUNT(T2.wins) FROM results AS T1 JOIN driverStandings AS T2 ON T1.driverId = T2.driverId WHERE T2.position = 91
SELECT T2.name FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId ORDER BY T1.fastestLapTime DESC LIMIT 1
SELECT T2.location, T2.country FROM races AS T1 JOIN circuits AS T2 ON T1.circuitId = T2.circuitId ORDER BY T1.date DESC LIMIT 1
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN qualifying AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T2.position = 1 AND T3.year = 2008 AND T3.circuitId IN (SELECT circuitId FROM circuits WHERE name = 'Marina Bay Street Circuit')
SELECT T1.forename, T1.surname, T1.nationality, T3.name FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.dob = ( SELECT MAX(dob) FROM drivers ) LIMIT 1
SELECT COUNT(*) FROM results WHERE raceId IN (SELECT raceId FROM races WHERE name = 'Canadian Grand Prix') AND statusId = 3
SELECT T1.wins, T2.forename, T2.surname FROM driverStandings AS T1 JOIN drivers AS T2 ON T1.driverId = T2.driverId ORDER BY T2.dob ASC LIMIT 1
SELECT MAX(duration) FROM pitStops
SELECT MIN(time) FROM lapTimes
SELECT MAX(T2.duration) FROM drivers AS T1 JOIN pitStops AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
SELECT T1.lap FROM pitStops AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T2.forename = 'Lewis' AND T2.surname = 'Hamilton' AND T3.name = 'Australian Grand Prix' AND T3.year = 2011
SELECT T1.duration FROM pitStops AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.year = 2011 AND T2.name = 'Australian Grand Prix'
SELECT T2.fastestLapTime FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
SELECT T2.forename, T2.surname FROM lapTimes AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId ORDER BY T1.time ASC LIMIT 20
SELECT T1.position FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN driverStandings AS T3 ON T1.driverId = T3.driverId JOIN drivers AS T4 ON T1.driverId = T4.driverId WHERE T4.forename = 'Lewis' AND T4.surname = 'Hamilton' ORDER BY T1.time ASC LIMIT 1
SELECT T1.time FROM lapTimes AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.name = 'Austrian Grand Prix' ORDER BY T1.milliseconds ASC LIMIT 1
SELECT T3.time FROM circuits AS T1 JOIN races AS T2 ON T1.circuitId = T2.circuitId JOIN lapTimes AS T3 ON T2.raceId = T3.raceId WHERE T1.country = 'Italy' ORDER BY T3.time ASC
SELECT T2.name FROM circuits AS T1 JOIN races AS T2 ON T1.circuitid = T2.circuitid JOIN results AS T3 ON T2.raceid = T3.raceid JOIN lapTimes AS T4 ON T3.raceid = T4.raceid WHERE T1.country = 'Austria' ORDER BY T4.milliseconds DESC LIMIT 1
SELECT T2.duration FROM races AS T1 JOIN pitStops AS T2 ON T1.raceId = T2.raceId WHERE T1.name = 'Austrian Grand Prix'
SELECT T3.lat, T3.lng FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId INNER JOIN circuits AS T3 ON T2.circuitId = T3.circuitId WHERE T1.fastestLapTime = '1:29.488'
SELECT AVG(T1.milliseconds) FROM pitStops AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T2.forename = 'Lewis' AND T2.surname = 'Hamilton'
SELECT AVG(T1.milliseconds) FROM lapTimes AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN circuits AS T3 ON T2.circuitId = T3.circuitId WHERE T3.country = 'Italy'
SELECT T1.player_api_id FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.overall_rating DESC LIMIT 1
SELECT T1.height, T1.player_name FROM Player AS T1 ORDER BY T1.height DESC LIMIT 1
SELECT preferred_foot FROM Player_Attributes WHERE potential = (SELECT MIN(potential) FROM Player_Attributes)
SELECT COUNT(id) FROM Player_Attributes WHERE overall_rating BETWEEN 60 AND 64 AND defensive_work_rate = 'low'
SELECT T2.player_api_id FROM Player_Attributes AS T1 JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.crossing DESC LIMIT 5
SELECT T2.name FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.season = '2015/2016' GROUP BY T2.name ORDER BY SUM(T1.home_team_goal + T1.away_team_goal) DESC LIMIT 1
SELECT T2.team_long_name FROM Match AS T1 INNER JOIN Team AS T2 ON T1.home_team_api_id = T2.id WHERE T1.season = '2015/2016' AND T1.home_team_goal - T1.away_team_goal < 0 GROUP BY T1.home_team_api_id ORDER BY COUNT(T1.home_team_goal - T1.away_team_goal) ASC LIMIT 1
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id GROUP BY T1.player_api_id ORDER BY SUM(T2.penalties) DESC LIMIT 10
SELECT T2.team_long_name FROM Match AS T1 INNER JOIN Team AS T2 ON T1.away_team_api_id = T2.team_api_id INNER JOIN League AS T3 ON T1.country_id = T3.id WHERE T1.season = '2009/2010' AND T3.name = 'Scotland Premier League' AND T1.away_team_goal - T1.home_team_goal > 0 GROUP BY T2.team_long_name ORDER BY COUNT(*) DESC LIMIT 1
SELECT buildUpPlaySpeed FROM Team_Attributes ORDER BY buildUpPlaySpeed DESC LIMIT 4
SELECT T2.name FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.season = '2015/2016' AND T1.home_team_goal = T1.away_team_goal GROUP BY T2.id ORDER BY COUNT(T1.id) DESC LIMIT 1
SELECT (strftime('%Y', 'now') - strftime('%Y', T1.birthday)) AS age FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.sprint_speed >= 97 AND strftime('%Y', T2.date) BETWEEN '2013' AND '2015'
SELECT T1.name, COUNT(T2.league_id) AS match_count FROM League AS T1 JOIN Match AS T2 ON T1.id = T2.league_id GROUP BY T2.league_id ORDER BY match_count DESC LIMIT 1
SELECT AVG(height) FROM Player WHERE birthday >= '1990-01-01 00:00:00' AND birthday < '1996-01-01 00:00:00'
SELECT player_api_id FROM Player_Attributes WHERE strftime('%Y', date) = '2010' AND overall_rating > ( SELECT AVG(overall_rating) FROM Player_Attributes WHERE strftime('%Y', date) = '2010' )
SELECT team_fifa_api_id FROM Team_Attributes WHERE buildUpPlaySpeed BETWEEN 51 AND 59
SELECT T1.team_long_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE strftime('%Y', T2.`date`) = '2012' AND T2.buildUpPlayPassing > ( SELECT AVG(buildUpPlayPassing) FROM Team_Attributes WHERE strftime('%Y', `date`) = '2012' ) AND T2.buildUpPlayPassing IS NOT NULL
SELECT CAST(SUM(CASE WHEN T1.preferred_foot = 'left' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE STRFTIME('%Y', T2.birthday) BETWEEN '1987' AND '1992'
SELECT T2.name, SUM(T1.home_team_goal + T1.away_team_goal) AS total_goals FROM Match AS T1 JOIN League AS T2 ON T1.league_id = T2.id GROUP BY T2.name ORDER BY total_goals ASC LIMIT 5
SELECT AVG(long_shots) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T1.player_name = 'Ahmed Samir Farag'
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T1.height > 180 GROUP BY T2.player_api_id ORDER BY AVG(T2.heading_accuracy) DESC LIMIT 10
SELECT T1.team_long_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlayDribblingClass = 'Normal' AND T2.date >= '2014-01-01 00:00:00' AND T2.date <= '2014-12-31 23:59:59' AND T2.chanceCreationPassing < ( SELECT AVG(chanceCreationPassing) FROM Team_Attributes WHERE buildUpPlayDribblingClass = 'Normal' AND date >= '2014-01-01 00:00:00' AND date <= '2014-12-31 23:59:59' ) ORDER BY T2.chanceCreationPassing DESC
SELECT T2.name FROM Match AS T1 INNER JOIN League AS T2 ON T1.country_id = T2.id WHERE T1.season = '2009/2010' GROUP BY T2.id HAVING AVG(T1.home_team_goal) > AVG(T1.away_team_goal)
SELECT team_short_name FROM Team WHERE team_long_name = 'Queens Park Rangers'
SELECT player_name FROM Player WHERE SUBSTR(birthday, 1, 4) = '1970' AND SUBSTR(birthday, 6, 2) = '10'
SELECT T2.attacking_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Franco Zennaro'
SELECT T2.buildUpPlayPositioningClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T1.team_long_name = 'ADO Den Haag'
SELECT T2.heading_accuracy FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.date = '2014-09-18 00:00:00' AND T1.player_name = 'Francois Affolter'
SELECT T2.overall_rating FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Gabriel Tamas' AND strftime('%Y', T2.date) = '2011'
SELECT COUNT(CASE WHEN T2.season = '2015/2016' AND T2.country_id = (SELECT id FROM Country WHERE name = 'Scotland') AND T1.name = 'Scotland Premier League' THEN T2.id END) FROM League AS T1 JOIN Match AS T2 ON T1.id = T2.league_id
SELECT T2.preferred_foot FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.birthday DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.potential IN (SELECT MAX(potential) FROM Player_Attributes)
SELECT COUNT(T1.player_api_id) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.weight < 130 AND T2.preferred_foot = 'left'
SELECT T2.team_short_name FROM Team_Attributes AS T1 INNER JOIN Team AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T1.chanceCreationPassingClass = 'Risky'
SELECT T2.defensive_work_rate FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'David Wilson'
SELECT T2.birthday FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.overall_rating DESC LIMIT 1
SELECT T1.name FROM League AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T2.name = 'Netherlands'
SELECT AVG(T1.home_team_goal) FROM Match AS T1 JOIN Country AS T2 ON T1.country_id = T2.id JOIN League AS T3 ON T1.league_id = T3.id WHERE T2.name = 'Poland' AND T1.season = '2010/2011'
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.height >= ( SELECT MIN(height) FROM Player WHERE height > 0 ) AND T1.height <= ( SELECT MAX(height) FROM Player ) GROUP BY T1.id ORDER BY AVG(T2.finishing) DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.height > 180
SELECT COUNT(id) FROM Player WHERE strftime('%Y', birthday) > '1990'
SELECT COUNT(*) FROM Player WHERE player_name LIKE 'Adam%' AND weight > 170
SELECT T2.player_name FROM Player_Attributes AS T1 JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.overall_rating > 80 AND strftime('%Y', T1.date) BETWEEN '2008' AND '2010'
SELECT T2.potential FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Aaron Doran'
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.preferred_foot = 'left'
SELECT T1.team_long_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlaySpeedClass = 'Fast'
SELECT T2.buildUpPlayPassingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_short_name = 'CLB'
SELECT T1.team_short_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T2.buildUpPlayPassing > 70
SELECT AVG(t2.overall_rating) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE strftime('%Y', t2.date) BETWEEN '2010' AND '2015' AND t1.height > 170
SELECT player_name FROM Player ORDER BY height ASC LIMIT 1
SELECT T2.name FROM League AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T1.name = 'Italy Serie A'
SELECT T1.team_short_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlaySpeed = 31 AND T2.buildUpPlayDribbling = 53 AND T2.buildUpPlayPassing = 32
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Aaron Doran'
SELECT COUNT(*) FROM League AS T2 JOIN Match AS T3 ON T2.id = T3.league_id WHERE T2.name = 'Germany 1. Bundesliga' AND strftime('%Y-%m', T3.date) BETWEEN '2008-08' AND '2008-10'
SELECT T2.team_short_name FROM Match AS T1 INNER JOIN Team AS T2 ON T1.home_team_api_id = T2.team_api_id WHERE T1.home_team_goal = 10
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.potential = 61 ORDER BY T2.balance DESC LIMIT 1
SELECT (AVG(CASE WHEN T1.player_name = 'Abdou Diallo' THEN T2.ball_control ELSE NULL END) - AVG(CASE WHEN T1.player_name = 'Aaron Appindangoye' THEN T2.ball_control ELSE NULL END)) AS difference FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id
SELECT team_long_name FROM Team WHERE team_short_name = 'GEN'
SELECT player_name FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday LIMIT 1
SELECT player_name FROM Player ORDER BY height DESC LIMIT 1
SELECT COUNT(id) FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
SELECT T2.name FROM League AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T1.name = 'Belgium Jupiler League'
SELECT T2.name FROM Country AS T1 JOIN League AS T2 ON T1.id = T2.country_id WHERE T1.name = 'Germany'
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.overall_rating DESC LIMIT 1
SELECT COUNT(DISTINCT T1.player_api_id) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE strftime('%Y', T1.birthday) < '1986' AND T2.defensive_work_rate = 'high'
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name IN ('Alexis', 'Ariel Borysiuk', 'Arouna Kone') ORDER BY T2.crossing DESC LIMIT 1
SELECT T2.heading_accuracy FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Ariel Borysiuk'
SELECT COUNT(T1.player_api_id) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.height > 180 AND T2.volleys > 70
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.volleys > 70 AND T2.dribbling > 70
SELECT COUNT(T1.id) FROM Match AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T1.season = '2008/2009' AND T2.name = 'Belgium'
SELECT T2.long_passing FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.birthday ASC LIMIT 1
SELECT COUNT(T1.id) FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T2.name = 'Belgium Jupiler League' AND SUBSTR(T1.`date`, 1, 7) = '2009-04'
SELECT T2.name FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.season = '2008/2009' GROUP BY T2.name ORDER BY COUNT(*) DESC LIMIT 1
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE strftime('%Y', T1.birthday) < '1986'
SELECT (CAST(SUM(CASE WHEN player_name = 'Ariel Borysiuk' THEN overall_rating ELSE 0 END) - SUM(CASE WHEN player_name = 'Paulin Puel' THEN overall_rating ELSE 0 END) AS REAL) * 100) / SUM(CASE WHEN player_name = 'Paulin Puel' THEN overall_rating ELSE 0 END) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id
SELECT AVG(buildUpPlaySpeed) FROM Team_Attributes WHERE team_fifa_api_id IN (SELECT team_fifa_api_id FROM Team WHERE team_long_name = 'Heart of Midlothian')
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Pietro Marino'
SELECT SUM(T2.crossing) FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Aaron Lennox'
SELECT T2.chanceCreationPassing, T2.chanceCreationPassingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Ajax' ORDER BY T2.chanceCreationPassing DESC LIMIT 1
SELECT T2.preferred_foot FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Abdou Diallo'
SELECT MAX(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Dorlan Pabon'
SELECT AVG(T1.away_team_goal) FROM Match AS T1 INNER JOIN Team AS T2 ON T2.team_api_id = T1.away_team_api_id INNER JOIN League AS T3 ON T3.id = T1.league_id INNER JOIN Country AS T4 ON T4.id = T3.country_id WHERE T2.team_long_name = 'Parma' AND T4.name = 'Italy'
SELECT T2.player_name FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.overall_rating = 77 AND T1.date LIKE '2016-06-23%' ORDER BY T2.birthday ASC LIMIT 1
SELECT T2.overall_rating FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Aaron Mooy' AND T2.date LIKE '2016-02-04%'
SELECT T2.potential FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Francesco Parravicini' AND T2.`date` = '2010-08-30 00:00:00'
SELECT T2.attacking_work_rate FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Francesco Migliore' AND T2.date LIKE '2015-05-01%'
SELECT T2.defensive_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Kevin Berigaud' AND T2.date = '2013-02-22 00:00:00'
SELECT T2.date FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Kevin Constant' ORDER BY T2.crossing DESC LIMIT 1
SELECT T2.buildUpPlaySpeedClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Willem II' AND T2.date = '2011-02-22 00:00:00'
SELECT T2.buildUpPlayDribblingClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.date = '2015-09-10 00:00:00' AND T1.team_short_name = 'LEI'
SELECT T2.buildUpPlayPassingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'FC Lorient' AND T2.`date` LIKE '2010-02-22%'
SELECT T2.chanceCreationPassingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'PEC Zwolle' AND T2.`date` = '2013-09-20 00:00:00'
SELECT T2.chanceCreationCrossingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Hull City' AND T2.`date` = '2010-02-22 00:00:00'
SELECT T2.defenceAggressionClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Hannover 96' AND T2.date LIKE '2015-09-10%'
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Marko Arnautovic' AND T2.date BETWEEN '2007-02-22' AND '2016-04-21'
SELECT (CAST(SUM(CASE WHEN T1.player_name = 'Landon Donovan' THEN T2.overall_rating ELSE 0 END) - SUM(CASE WHEN T1.player_name = 'Jordan Bowery' THEN T2.overall_rating ELSE 0 END) AS REAL) * 100) / SUM(CASE WHEN T1.player_name = 'Landon Donovan' THEN T2.overall_rating ELSE 0 END) FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.`date` = '2013-07-12 00:00:00'
SELECT player_name FROM Player ORDER BY height DESC LIMIT 1
SELECT player_api_id FROM Player ORDER BY weight DESC LIMIT 10
SELECT player_name FROM Player WHERE (datetime(CURRENT_TIMESTAMP, 'localtime') - datetime(birthday)) > 34
SELECT SUM(CASE WHEN T1.home_team_goal > 0 THEN 1 ELSE 0 END) FROM Match AS T1 INNER JOIN Player AS T2 ON T1.home_player_1 = T2.player_api_id WHERE T2.player_name = 'Aaron Lennon'
SELECT SUM(CASE WHEN T2.player_name = 'Daan Smith' THEN T1.away_team_goal ELSE 0 END) + SUM(CASE WHEN T2.player_name = 'Filipe Ferreira' THEN T1.away_team_goal ELSE 0 END) AS total_away_goals FROM Match AS T1 INNER JOIN Player AS T2 ON T1.away_player_1 = T2.player_api_id
SELECT SUM(home_team_goal) FROM Match INNER JOIN Player ON Match.home_player_1 = Player.player_api_id WHERE (datetime(CURRENT_TIMESTAMP, 'localtime') - datetime(Player.birthday)) / 365 < 30
SELECT T2.player_name FROM Player_Attributes AS T1 JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.overall_rating DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.potential DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.attacking_work_rate = 'high'
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.finishing = 1 ORDER BY (CURRENT_TIMESTAMP - T1.birthday) DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 JOIN Match AS T2 ON T1.player_api_id = T2.home_player_1 JOIN Country AS T3 ON T2.country_id = T3.id WHERE T3.name = 'Belgium'
SELECT T3.name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id JOIN Country AS T3 ON T1.birthday LIKE '%-%-%' WHERE T2.vision > 89
SELECT T2.name FROM Player AS T1 INNER JOIN Country AS T2 ON T1.player_fifa_api_id = T2.id GROUP BY T2.name ORDER BY AVG(T1.weight) DESC LIMIT 1
SELECT T1.team_long_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T2.buildUpPlaySpeedClass = 'Slow'
SELECT T3.team_short_name FROM Team_Attributes AS T1 INNER JOIN Match AS T2 ON T1.team_api_id = T2.home_team_api_id INNER JOIN Team AS T3 ON T1.team_api_id = T3.id WHERE T1.chanceCreationPassingClass = 'Safe' UNION ALL SELECT T3.team_short_name FROM Team_Attributes AS T1 INNER JOIN Match AS T2 ON T1.team_api_id = T2.away_team_api_id INNER JOIN Team AS T3 ON T1.team_api_id = T3.id WHERE T1.chanceCreationPassingClass = 'Safe'
SELECT AVG(T1.height) FROM Player AS T1 JOIN Match AS T3 ON T1.player_api_id = T3.home_player_1 JOIN League AS T2 ON T3.league_id = T2.id JOIN Country AS T4 ON T2.country_id = T4.id WHERE T4.name = 'Italy'
SELECT player_name FROM Player WHERE height > 180 ORDER BY player_name ASC LIMIT 3
SELECT COUNT(player_name) FROM Player WHERE player_name LIKE 'Aaron%' AND birthday > '1990-01-01'
SELECT (SELECT jumping FROM Player_Attributes WHERE id = 6) - (SELECT jumping FROM Player_Attributes WHERE id = 23) AS jump_difference
SELECT player_api_id FROM Player_Attributes WHERE preferred_foot = 'right' ORDER BY potential ASC LIMIT 5
SELECT COUNT(T1.player_api_id) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.crossing = ( SELECT MAX(crossing) FROM Player_Attributes ) AND T1.preferred_foot = 'left'
SELECT CAST(COUNT(CASE WHEN stamina > 80 AND strength > 80 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM Player_Attributes
SELECT T1.name FROM Country AS T1 INNER JOIN League AS T2 ON T1.id = T2.country_id WHERE T2.name = 'Poland Ekstraklasa'
SELECT T1.home_team_goal, T1.away_team_goal FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.date LIKE '2008-09-24%' AND T2.name = 'Belgium Jupiler League'
SELECT T1.sprint_speed, T1.agility, T1.acceleration FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Alexis Blin'
SELECT T2.buildUpPlaySpeedClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'KSV Cercle Brugge'
SELECT COUNT(T1.id) FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.season = '2015/2016' AND T2.name LIKE '%Serie A%'
SELECT MAX(T1.home_team_goal) FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T2.name = 'Netherlands Eredivisie'
SELECT T1.finishing, T1.curve FROM Player_Attributes AS T1 JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.weight DESC LIMIT 1
SELECT T2.name FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T1.season = '2015/2016' GROUP BY T2.name ORDER BY COUNT(T1.id) DESC LIMIT 4
SELECT T2.team_long_name FROM Match AS T1 JOIN Team AS T2 ON T1.away_team_api_id = T2.team_api_id ORDER BY T1.away_team_goal DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.overall_rating DESC LIMIT 1
SELECT CAST(SUM(CASE WHEN T1.height < 180 AND T2.overall_rating > 70 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id
SELECT (CAST(COUNT(CASE WHEN T1.Admission = '+' THEN T1.ID ELSE NULL END) AS REAL) * 100) / COUNT(T1.ID) - (CAST(COUNT(CASE WHEN T1.Admission = '-' THEN T1.ID ELSE NULL END) AS REAL) * 100) / COUNT(T1.ID) AS PercentageDeviation FROM Patient AS T1 WHERE T1.SEX = 'M'
SELECT CAST(SUM(CASE WHEN STRFTIME('%Y', Birthday) > '1930' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(ID) FROM Patient WHERE SEX = 'F'
SELECT CAST(SUM(CASE WHEN Admission = '+' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(ID) FROM Patient WHERE Birthday BETWEEN '1930-01-01' AND '1940-12-31'
SELECT CAST(SUM(CASE WHEN Admission = '-' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN Admission = '+' THEN 1 ELSE 0 END) FROM Patient WHERE Diagnosis = 'SLE'
SELECT T1.Diagnosis, T2.Date FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.ID = 30609
SELECT T1.SEX, T1.Birthday, T2.`Examination Date`, T2.Symptoms FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = 163109
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.LDH > 500
SELECT T2.ID, strftime('%Y', 'now') - strftime('%Y', T2.Birthday) AS Age FROM Patient AS T2 INNER JOIN Examination AS T1 ON T2.ID = T1.ID WHERE T1.RVVT = '+'
SELECT DISTINCT p.ID, p.SEX, p.Diagnosis FROM Patient p JOIN Examination e ON p.ID = e.ID WHERE e.Thrombosis = 2
SELECT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE strftime('%Y', T1.Birthday) = '1937' AND T2.`T-CHO` >= 250
SELECT P.ID, P.SEX, P.Diagnosis  FROM Patient P  JOIN Laboratory L ON P.ID = L.ID  WHERE L.ALB < 3.5
SELECT (CAST(COUNT(CASE WHEN T2.TP < 6.0 OR T2.TP > 8.5 THEN T1.ID ELSE NULL END) AS REAL) * 100) / COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F'
SELECT AVG(T2.`aCL IgG`) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '+' AND (STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.Birthday)) >= 50
SELECT COUNT(ID) FROM Patient WHERE SEX = 'F' AND STRFTIME('%Y', Description) = '1997' AND Admission = '-'
SELECT MIN(strftime('%Y', T1.`First Date`) - strftime('%Y', T1.Birthday)) FROM Patient AS T1
SELECT COUNT(T1.ID) FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.SEX = 'F' AND T1.`Thrombosis` = 1 AND strftime('%Y', T1.`Examination Date`) = '1997'
SELECT (MAX(strftime('%Y', T1.Birthday)) - MIN(strftime('%Y', T1.Birthday))) AS AgeGap FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TG >= 200
SELECT T1.Symptoms, T1.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.Symptoms IS NOT NULL ORDER BY T2.Birthday DESC LIMIT 1
SELECT CAST(COUNT(T2.ID) AS REAL) / 12 FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`Date` BETWEEN '1998-01-01' AND '1998-12-31' AND T1.SEX = 'M'
SELECT T2.`Date`, (strftime('%Y', T1.`First Date`) - strftime('%Y', T1.Birthday)) AS Age FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SJS' ORDER BY Age DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN T1.SEX = 'M' THEN T1.ID ELSE NULL END) AS REAL) / COUNT(CASE WHEN T1.SEX = 'F' THEN T1.ID ELSE NULL END) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.UA < (CASE WHEN T1.SEX = 'M' THEN 8 ELSE 6.5 END)
SELECT COUNT(DISTINCT Patient.ID) FROM Patient JOIN Examination ON Patient.ID = Examination.ID WHERE strftime('%Y', Examination.`Examination Date`) - strftime('%Y', Patient.`First Date`) >= 1
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 JOIN Examination AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Birthday) < '1990' AND STRFTIME('%Y', T2.`Examination Date`) BETWEEN '1990' AND '1993'
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.`T-BIL` >= 2.0
SELECT T2.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`Examination Date` BETWEEN '1985-01-01' AND '1995-12-31' GROUP BY T2.Diagnosis ORDER BY COUNT(T2.Diagnosis) DESC LIMIT 1
SELECT AVG(1999 - STRFTIME('%Y', T1.Birthday)) AS AverageAge FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`Date` BETWEEN '1991-10-01' AND '1991-10-30'
SELECT (STRFTIME('%Y', T1.`Examination Date`) - STRFTIME('%Y', T3.Birthday)) AS Age, T3.Diagnosis FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID INNER JOIN Patient AS T3 ON T1.ID = T3.ID ORDER BY T2.HGB DESC LIMIT 1
SELECT ANA FROM Examination WHERE ID = 3605340 AND `Examination Date` = '1996-12-02'
SELECT CASE WHEN T1.`T-CHO` < 250 THEN 'Normal' ELSE 'Abnormal' END AS Status FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`Date` = '1995-09-04' AND T2.ID = 2927464
SELECT SEX FROM Patient WHERE Diagnosis = 'AORTITIS' ORDER BY `First Date` ASC LIMIT 1
SELECT T2.`aCL IgM` FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T1.Description = '1994-02-19' AND T2.`Examination Date` = '1993-11-12'
SELECT T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`Date` = '1992-06-12' AND T2.GPT = 9
SELECT (STRFTIME('%Y', Laboratory.Date) - STRFTIME('%Y', Patient.Birthday)) AS Age FROM Laboratory INNER JOIN Patient ON Laboratory.ID = Patient.ID WHERE Laboratory.Date = '1991-10-21' AND Laboratory.UA = '8.4'
SELECT COUNT(ID) FROM Laboratory WHERE ID IN (SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS') AND `Date` LIKE '1995%'
SELECT T2.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`Examination Date` = '1997-01-27' AND T2.Diagnosis = 'SLE' ORDER BY T2.`First Date` ASC LIMIT 1
SELECT T2.Symptoms FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Birthday = '1959-03-01' AND T2.`Examination Date` = '1993-09-27'
SELECT SUM(CASE WHEN T1.Birthday = '1959-02-18' AND T2.`Date` LIKE '1981-11-%' THEN `T-CHO` ELSE 0 END) - SUM(CASE WHEN T1.Birthday = '1959-02-18' AND T2.`Date` LIKE '1981-12-%' THEN `T-CHO` ELSE 0 END) AS DecreaseRate FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID
SELECT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'BEHCET' AND T1.Description BETWEEN '1997-01-01' AND '1997-12-31'
SELECT DISTINCT ID FROM Laboratory WHERE `Date` BETWEEN '1987-07-06' AND '1996-01-31' AND GPT > 30 AND ALB < 4
SELECT ID FROM Patient WHERE SEX = 'F' AND strftime('%Y', Birthday) = '1964' AND Admission = '+'
SELECT COUNT(*) FROM Examination WHERE Thrombosis = 2 AND `ANA Pattern` = 'S' AND `aCL IgM` > (SELECT AVG(`aCL IgM`) FROM Examination WHERE Thrombosis = 2 AND `ANA Pattern` = 'S') * 1.2
SELECT CAST(SUM(CASE WHEN UA < 6.5 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(ID) FROM Laboratory WHERE `U-PRO` > 0 AND `U-PRO` < 30
SELECT CAST(COUNT(CASE WHEN Diagnosis = 'BEHCET' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM Patient WHERE STRFTIME('%Y', `First Date`) = '1981' AND SEX = 'M'
SELECT DISTINCT T1.ID FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.`Date` LIKE '1991-10%' AND T2.`T-BIL` < 2.0
SELECT COUNT(*) FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`ANA Pattern` != 'P' AND T2.SEX = 'F' AND T2.Birthday BETWEEN '1980-01-01' AND '1989-12-31'
SELECT T3.SEX FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID JOIN Patient AS T3 ON T2.ID = T3.ID WHERE T1.Diagnosis = 'PSS' AND T2.CRP LIKE '2+' AND T2.CRE = 1 AND T2.LDH = 123
SELECT AVG(T2.ALB) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND T2.PLT > 400 AND T1.Diagnosis = 'SLE'
SELECT Symptoms FROM Examination WHERE Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1
SELECT Description, Diagnosis FROM Patient WHERE ID = 48473
SELECT COUNT(ID) FROM Patient WHERE SEX = 'F' AND Diagnosis = 'APS'
SELECT COUNT(T2.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T2.`Date`) = '1997' AND (T2.TP < 6 OR T2.TP > 8.5)
SELECT CAST(SUM(CASE WHEN T1.Diagnosis LIKE '%SLE%' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.Symptoms LIKE '%thrombocytopenia%'
SELECT CAST(COUNT(CASE WHEN SEX = 'F' THEN ID ELSE NULL END) AS REAL) * 100 / COUNT(ID) FROM Patient WHERE STRFTIME('%Y', Birthday) = '1980' AND Diagnosis = 'RA'
SELECT COUNT(T1.ID) FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.SEX = 'M' AND T1.`Examination Date` BETWEEN '1995-01-01' AND '1997-12-31' AND T2.Diagnosis = 'BEHCET' AND T2.Admission = '-'
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND T2.WBC < 3.5
SELECT strftime('%J', T2.`Examination Date`) - strftime('%J', T1.`First Date`) AS days_difference FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = 821298
SELECT CASE WHEN T1.UA > 8.0 AND T2.SEX = 'M' THEN 'Yes' WHEN T1.UA > 6.5 AND T2.SEX = 'F' THEN 'Yes' ELSE 'No' END AS NormalRange FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.ID = 57266
SELECT T2.`Date` FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.ID = 48473 AND T2.GOT >= 60
SELECT T2.SEX, T2.Birthday FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE strftime('%Y', T1.`Date`) = '1994' AND T1.GOT < 60
SELECT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.GPT >= 60
SELECT T1.Diagnosis FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GPT > 60 ORDER BY T1.Birthday ASC
SELECT AVG(LDH) FROM Laboratory WHERE LDH < 500
SELECT T1.ID, (strftime('%Y', 'now') - strftime('%Y', T1.Birthday)) AS Age FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.LDH BETWEEN 600 AND 800
SELECT T2.Admission FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.ALP < 300
SELECT T1.ID, CASE WHEN T2.ALP < 300 THEN 'Yes' ELSE 'No' END AS ALP_within_range FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Birthday = '1982-04-01'
SELECT T2.ID, T2.SEX, T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TP < 6.0
SELECT T2.TP - 8.5 AS deviation FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND T2.TP > 8.5
SELECT T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND (T2.ALB < 3.5 OR T2.ALB > 5.5) ORDER BY T1.Birthday DESC
SELECT CASE WHEN T1.Birthday BETWEEN '1982-01-01' AND '1982-12-31' AND T2.ALB BETWEEN 3.5 AND 5.5 THEN 'Yes' ELSE 'No' END AS Albumin_Within_Normal_Range FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID
SELECT CAST(SUM(CASE WHEN SEX = 'F' AND UA > 6.5 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(Sex) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.SEX = 'F'
SELECT AVG(L1.UA) FROM Laboratory AS L1 INNER JOIN Patient AS P1 ON L1.ID = P1.ID WHERE (P1.SEX = 'M' AND L1.UA < 8.0) OR (P1.SEX = 'F' AND L1.UA < 6.5)
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.UN = 29
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'RA' AND T2.UN < 30
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CRE >= 1.5 AND T1.SEX = 'M'
SELECT CASE WHEN SUM(CASE WHEN T1.SEX = 'M' THEN 1 ELSE 0 END) > SUM(CASE WHEN T1.SEX = 'F' THEN 1 ELSE 0 END) THEN 1 ELSE 0 END AS is_more_male FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CRE >= 1.5
SELECT T2.ID, T2.SEX, T2.Birthday FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID ORDER BY T1.`T-BIL` DESC LIMIT 1
SELECT t1.SEX, GROUP_CONCAT(DISTINCT t1.ID) FROM Patient AS t1 INNER JOIN Laboratory AS t2 ON t1.ID = t2.ID WHERE t2.`T-BIL` >= 2.0 GROUP BY t1.SEX
SELECT T1.ID, T2.`T-CHO` FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID ORDER BY T1.Birthday ASC, T2.`T-CHO` DESC LIMIT 1
SELECT AVG((strftime('%Y', 'now')) - strftime('%Y', Patient.Birthday)) AS average_age FROM Patient JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Patient.SEX = 'M' AND Laboratory.`T-CHO` >= 250
SELECT T2.ID, T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TG > 300
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TG >= 200 AND (STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.Birthday)) > 50
SELECT DISTINCT T2.ID FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.CPK < 250
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Birthday) BETWEEN '1936' AND '1956' AND T1.SEX = 'M' AND T2.CPK >= 250
SELECT T1.ID, T1.SEX, (STRFTIME('%Y', 'now') - STRFTIME('%Y', T1.Birthday)) AS age FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GLU >= 180 AND T2.`T-CHO` < 250
SELECT T1.ID, T2.GLU FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Description) = '1991' AND T2.GLU < 180
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T2.WBC < 3.5) OR (T2.WBC >= 9.0) GROUP BY T1.SEX ORDER BY (date('now') - T1.Birthday) ASC
SELECT T1.Diagnosis, T1.ID, (STRFTIME('%Y', 'now') - STRFTIME('%Y', T1.Birthday)) AS Age FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RBC < 3.5
SELECT P.Admission FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE P.SEX = 'F' AND (STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', P.Birthday)) >= 50 AND (L.RBC <= 3.5 OR L.RBC >= 6.0)
SELECT DISTINCT T1.ID, T1.SEX FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.HGB < 10
SELECT T1.ID, T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND 10 < T2.HGB < 17 ORDER BY T1.Birthday ASC LIMIT 1
SELECT T1.ID, STRFTIME('%Y', 'now') - STRFTIME('%Y', T2.Birthday) AS Age FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.HCT >= 52 GROUP BY T1.ID HAVING COUNT(T1.ID) > 2
SELECT AVG(HCT) FROM Laboratory WHERE `Date` LIKE '1991%' AND HCT < 29
SELECT SUM(CASE WHEN PLT < 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN PLT > 400 THEN 1 ELSE 0 END) AS PlateletBalance FROM Laboratory
SELECT T2.ID FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Date) = '1984' AND (STRFTIME('%Y', 'now') - STRFTIME('%Y', T2.Birthday)) < 50 AND T1.PLT BETWEEN 100 AND 400
SELECT CAST(SUM(CASE WHEN T1.SEX = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (STRFTIME('%Y', 'now') - STRFTIME('%Y', T1.Birthday)) > 55 AND T2.PT >= 14
SELECT T1.ID FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.`First Date`) > '1992' AND T2.PT < 14
SELECT COUNT(*) - ( SELECT COUNT(*) FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.`Examination Date` > '1997-01-01' AND T2.APTT < 45 ) AS Inactivated_Partial_Protehembin_Time FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.`Examination Date` > '1997-01-01'
SELECT COUNT(DISTINCT T1.ID) FROM Examination AS T2 INNER JOIN Laboratory AS T1 ON T1.ID = T2.ID WHERE T1.APTT > 45 AND T2.Thrombosis = 0
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.WBC > 3.5 AND T2.WBC < 9.0 AND (T2.FG < 150 OR T2.FG >= 450)
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Birthday > '1980-01-01' AND (T2.FG < 150 OR T2.FG > 450)
SELECT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`U-PRO` >= 30
SELECT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`U-PRO` BETWEEN 0 AND 30 AND T1.Diagnosis = 'SLE'
SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE IGG >= 2000
SELECT COUNT(*) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGG > 900 AND T2.IGG < 2000 AND T1.Symptoms IS NOT NULL
SELECT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.IGA BETWEEN 80 AND 500 ORDER BY T1.IGA DESC LIMIT 1
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.IGA > 80 AND T1.IGA < 500 AND STRFTIME('%Y', T2.`First Date`) >= '1990'
SELECT T1.Diagnosis FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM <= 40 OR T2.IGM >= 400 GROUP BY T1.Diagnosis ORDER BY COUNT(*) DESC LIMIT 1
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.CRP = '+' AND T2.Description IS NULL
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.CRE >= 1.5 AND (strftime('%Y', 'now') - strftime('%Y', T2.Birthday)) < 70
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.RA IN ('-', '+-') AND T2.KCT = '+'
SELECT DISTINCT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Birthday) >= '1985' AND T2.RA IN ('-', '+-')
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RF < 20 AND (strftime('%Y', 'now') - strftime('%Y', T1.Birthday)) > 60
SELECT COUNT(T1.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.RF < 20 AND T2.Thrombosis = 0
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.C3 > 35 AND T2.`ANA Pattern` = 'P'
SELECT T1.ID FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.HCT NOT BETWEEN 29 AND 52 ORDER BY T2.`aCL IgA` DESC LIMIT 1
SELECT COUNT(DISTINCT p.ID) FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.Admission = '+' AND l.C4 > 10
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RNP IN ('-', '+-') AND T1.Admission = '+'
SELECT T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RNP NOT IN ('-', '+-') ORDER BY T1.Birthday DESC LIMIT 1
SELECT COUNT(DISTINCT T2.ID) FROM Examination AS T2 INNER JOIN Laboratory AS T1 ON T1.ID = T2.ID WHERE T2.Thrombosis = 0 AND T1.SM IN ('negative', '0')
SELECT P.ID FROM Patient AS P JOIN Laboratory AS L ON P.ID = L.ID WHERE L.SM NOT IN ('negative', '0') ORDER BY P.Birthday DESC LIMIT 3
SELECT DISTINCT T2.ID FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.`Examination Date` > '1997-01-01' AND T1.KCT IN ('+', '-')
SELECT COUNT(DISTINCT T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID INNER JOIN Examination AS T3 ON T2.ID = T3.ID WHERE T1.SC170 IN ('negative', '0') AND T2.SEX = 'F' AND T3.Symptoms IS NULL
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.SSA IN (0, 1) AND STRFTIME('%Y', T1.`First Date`) < '2000'
SELECT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.`First Date` IS NOT NULL AND T2.SSA NOT IN ('negative', '0') ORDER BY T1.`First Date` ASC LIMIT 1
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.SSB IN ('negative', '0') AND T2.Diagnosis = 'SLE'
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.SSB IN ('negative', '0') AND T2.Symptoms IS NOT NULL
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CENTROMEA IN ('-', '+-') AND T2.SSB IN ('-', '+-') AND T1.SEX = 'M'
SELECT DISTINCT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.DNA >= 8
SELECT COUNT(DISTINCT T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.DNA < 8 AND T2.Description IS NULL
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.IGG > 900 AND T1.IGG < 2000 AND T2.Admission = '+'
SELECT CAST(SUM(CASE WHEN T1.Diagnosis = 'SLE' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.ID) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GOT >= 60
SELECT COUNT(T2.id) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.GOT < 60
SELECT T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.GOT >= 60 ORDER BY T2.Birthday DESC LIMIT 1
SELECT DISTINCT T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.GPT < 60 ORDER BY T1.GPT DESC LIMIT 3
SELECT COUNT(T2.ID) FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.GOT < 60 AND T2.SEX = 'M'
SELECT T2.`First Date` FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.LDH < 500 ORDER BY T1.LDH DESC LIMIT 1
SELECT T2.`Date` FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.LDH >= 500 ORDER BY T1.`First Date` DESC LIMIT 1
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.ALP >= 300 AND T2.Admission = '+'
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.ALP < 300
SELECT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TP < 6.0
SELECT COUNT(T1.ID) FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SJS' AND T2.TP BETWEEN 6.0 AND 8.5
SELECT T1.`Examination Date` FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.ALB BETWEEN 3.5 AND 5.5 ORDER BY T2.ALB DESC LIMIT 1
SELECT COUNT(*) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.ALB BETWEEN 3.5 AND 5.5 AND T2.TP BETWEEN 6.0 AND 8.5
SELECT T1.`aCL IgG`, T1.`aCL IgM`, T1.`aCL IgA` FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID JOIN Patient AS T3 ON T1.ID = T3.ID WHERE T2.UA > 6.50 AND T3.SEX = 'F' ORDER BY T2.UA DESC LIMIT 1
SELECT MAX(T1.ANA) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CRE < 1.5
SELECT T1.ID FROM Laboratory AS T1 JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.CRE < 1.5 ORDER BY T2.`aCL IgA` DESC LIMIT 1
SELECT COUNT(*) FROM Laboratory AS L JOIN Examination AS E ON L.ID = E.ID WHERE L.`T-BIL` >= 2.0 AND E.`ANA Pattern` LIKE '%P%'
SELECT T1.ANA FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`T-BIL` < 2.0 ORDER BY T2.`T-BIL` DESC LIMIT 1
SELECT COUNT(*) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.`T-CHO` >= 250 AND T2.KCT = '-'
SELECT COUNT(T1.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.`T-CHO` < 250 AND T2.`ANA Pattern` = 'P'
SELECT COUNT(T1.ID) FROM Examination AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TG < 200 AND T1.Symptoms IS NOT NULL
SELECT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TG < 200 ORDER BY T1.TG DESC LIMIT 1
SELECT T3.ID FROM Patient AS T3 INNER JOIN Examination AS T1 ON T3.ID = T1.ID INNER JOIN Laboratory AS T2 ON T3.ID = T2.ID WHERE T1.Thrombosis = 0 AND T2.CPK < 250
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.CPK < 250 AND (T2.KCT = '+' OR T2.RVVT = '+' OR T2.LAC = '+')
SELECT T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GLU > 180 ORDER BY T1.Birthday ASC LIMIT 1
SELECT COUNT(*) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.GLU < 180 AND T2.Thrombosis = 0
SELECT COUNT(*) FROM Laboratory AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.Admission = '+' AND T1.WBC BETWEEN 3.5 AND 9.0
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T2.WBC BETWEEN 3.5 AND 9.0
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T2.RBC < 3.5 OR T2.RBC > 6.0) AND T1.Admission = '-'
SELECT COUNT(T1.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.PLT > 100 AND T1.PLT < 400 AND T2.Diagnosis IS NOT NULL
SELECT T2.PLT FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'MCTD' AND T2.PLT > 100 AND T2.PLT < 400
SELECT AVG(T2.PT) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.PT < 14
SELECT COUNT(T1.ID) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Thrombosis = 1 AND T2.PT < 14
SELECT T2.major_name FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Angela' AND T1.last_name = 'Sanders'
SELECT COUNT(*) FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major WHERE T1.college = 'College of Engineering'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.department = 'Art and Design Department' AND T1.position = 'Member'
SELECT COUNT(DISTINCT T3.member_id) FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.event_name = 'Women''s Soccer'
SELECT DISTINCT T3.phone  FROM event AS T1  JOIN attendance AS T2 ON T1.event_id = T2.link_to_event  JOIN member AS T3 ON T2.link_to_member = T3.member_id  WHERE T1.event_name = 'Women''s Soccer'
SELECT COUNT(*)  FROM event AS e  JOIN attendance AS a ON e.event_id = a.link_to_event  JOIN member AS m ON a.link_to_member = m.member_id  WHERE e.event_name = 'Women''s Soccer' AND m.t_shirt_size = 'Medium'
SELECT T1.event_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event GROUP BY T1.event_id ORDER BY COUNT(T2.link_to_member) DESC LIMIT 1
SELECT T2.college FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'Vice President'
SELECT T3.event_name FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T1.first_name = 'Maya' AND T1.last_name = 'Mclean'
SELECT COUNT(T1.event_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE STRFTIME('%Y', T1.event_date) = '2019' AND T3.first_name = 'Sacha' AND T3.last_name = 'Harrison'
SELECT COUNT(T1.event_id) FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event GROUP BY T2.link_to_event HAVING COUNT(T2.link_to_member) > 10 AND T1.type = 'Meeting'
SELECT T1.event_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN budget AS T3 ON T1.event_id = T3.link_to_event WHERE T3.category != 'Fundraising' GROUP BY T1.event_id HAVING COUNT(T2.link_to_member) > 20
SELECT CAST(COUNT(T1.event_id) AS REAL) / COUNT(DISTINCT T1.event_name) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE STRFTIME('%Y', T1.event_date) = '2020' AND T1.type = 'Meeting'
SELECT expense_description FROM expense WHERE cost = (SELECT MAX(cost) FROM expense)
SELECT COUNT(T1.member_id) FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Environmental Engineering'
SELECT T3.first_name, T3.last_name FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T3.member_id = T2.link_to_member WHERE T1.event_name = 'Laugh Out Loud'
SELECT T1.last_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Law and Constitutional Studies'
SELECT T2.county FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Sherri' AND T1.last_name = 'Ramsey'
SELECT T2.college FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Tyler' AND T1.last_name = 'Hewitt'
SELECT T2.amount FROM member AS T1 JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.`position` = 'Vice President'
SELECT T1.spent FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.event_name = 'September Meeting' AND T1.category = 'Food'
SELECT T2.city, T2.state FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.position = 'President'
SELECT T1.first_name, T1.last_name FROM member AS T1 JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.state = 'Illinois'
SELECT SUM(T2.spent) FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'September Meeting' AND T2.category = 'Advertisement'
SELECT T1.department FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major WHERE T2.last_name = 'Pierce' OR T2.last_name = 'Guidi'
SELECT SUM(T2.amount) FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'October Speaker'
SELECT T2.approved FROM event AS T1 INNER JOIN expense AS T2 ON T1.event_id = T2.link_to_budget WHERE T1.event_date = '2019-10-08' AND T1.event_name = 'October Meeting'
SELECT AVG(T2.cost) FROM member AS T1 JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE STRFTIME('%m', T2.expense_date) IN ('09', '10') AND T1.first_name = 'Elijah' AND T1.last_name = 'Allen'
SELECT (SUM(CASE WHEN SUBSTR(T1.event_date, 1, 4) = '2019' THEN T2.spent ELSE 0 END) - SUM(CASE WHEN SUBSTR(T1.event_date, 1, 4) = '2020' THEN T2.spent ELSE 0 END)) AS difference FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event
SELECT location FROM event WHERE event_name = 'Spring Budget Review'
SELECT T1.cost FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id WHERE T1.expense_description = 'Posters' AND T1.expense_date = '2019-09-04'
SELECT remaining FROM budget WHERE category = 'Food' AND amount = (SELECT MAX(amount) FROM budget WHERE category = 'Food')
SELECT notes FROM income WHERE date_received = '2019-09-14' AND source = 'Fundraising'
SELECT COUNT(major_id) FROM major WHERE college = 'College of Humanities and Social Sciences'
SELECT phone FROM member WHERE first_name = 'Carlo' AND last_name = 'Jacobs'
SELECT T2.county FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Adela' AND T1.last_name = 'O''Gallagher'
SELECT COUNT(*) FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.event_name = 'November Meeting' AND T1.remaining < 0
SELECT SUM(T2.amount) FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'September Speaker'
SELECT T2.event_status FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id WHERE T1.expense_date = '2019-08-20' AND T1.expense_description = 'Post Cards, Posters'
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Brent' AND T1.last_name = 'Thomason'
SELECT COUNT(m.member_id) FROM member m INNER JOIN major ma ON m.link_to_major = ma.major_id WHERE ma.major_name = 'Business' AND m.t_shirt_size = 'Medium'
SELECT T2.type FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Christof' AND T1.last_name = 'Nielson'
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.`position` = 'Vice President'
SELECT T2.state FROM member AS T1 JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Sacha' AND T1.last_name = 'Harrison'
SELECT T2.department FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'President'
SELECT T2.date_received FROM member AS T1 JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.first_name = 'Connor' AND T1.last_name = 'Hilton' AND T2.source = 'Dues'
SELECT T2.first_name, T2.last_name FROM income AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.source = 'Dues' ORDER BY T1.date_received ASC LIMIT 1
SELECT CAST(SUM(CASE WHEN T2.event_name = 'Yearly Kickoff' THEN amount ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.event_name = 'October Meeting' THEN amount ELSE 0 END) FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.category = 'Advertisement'
SELECT (CAST(SUM(CASE WHEN T1.category = 'Parking' THEN T1.amount ELSE 0 END) AS REAL) * 100) / SUM(T1.amount) FROM budget AS T1 JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.event_name = 'November Speaker'
SELECT SUM(cost) FROM expense WHERE expense_description = 'Pizza'
SELECT COUNT(city) FROM zip_code WHERE county = 'Orange County' AND state = 'Virginia'
SELECT department FROM major WHERE college = 'College of Humanities and Social Sciences'
SELECT T2.city, T2.county, T2.state FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Amy' AND T1.last_name = 'Firth'
SELECT T2.expense_description FROM budget AS T1 INNER JOIN expense AS T2 ON T1.budget_id = T2.link_to_budget ORDER BY T1.remaining ASC LIMIT 1
SELECT m.first_name, m.last_name FROM event e INNER JOIN attendance a ON e.event_id = a.link_to_event INNER JOIN member m ON a.link_to_member = m.member_id WHERE e.event_name = 'October Meeting'
SELECT T1.college FROM major AS T1 JOIN member AS T2 ON T1.major_id = T2.link_to_major GROUP BY T1.college ORDER BY COUNT(T1.major_id) DESC LIMIT 1
SELECT T2.major_name FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.phone = '809-555-3360'
SELECT T1.event_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event ORDER BY T2.amount DESC LIMIT 1
SELECT T1.expense_description FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T2.position = 'Vice President'
SELECT COUNT(T2.link_to_member) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'Women''s Soccer'
SELECT T2.date_received FROM member AS T1 JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.first_name = 'Casey' AND T1.last_name = 'Mason'
SELECT COUNT(T1.member_id) FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.state = 'Maryland'
SELECT COUNT(T2.link_to_event) FROM member AS T1 JOIN attendance AS T2 ON T1.member_id = T2.link_to_member WHERE T1.phone = '954-555-6240'
SELECT T2.first_name, T2.last_name FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major WHERE T1.department = 'School of Applied Sciences, Technology and Education'
SELECT T1.event_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.status = 'Closed' ORDER BY CAST(T2.spent AS REAL) / T2.amount DESC LIMIT 1
SELECT COUNT(member_id) FROM member WHERE `position` = 'President'
SELECT MAX(spent) FROM budget
SELECT COUNT(event_id) FROM event WHERE type = 'Meeting' AND strftime('%Y', event_date) = '2020'
SELECT SUM(spent) FROM budget WHERE category = 'Food'
SELECT T2.first_name, T2.last_name FROM attendance AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id GROUP BY T2.member_id HAVING COUNT(T1.link_to_event) > 7
SELECT T3.first_name, T3.last_name FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event JOIN member AS T3 ON T2.link_to_member = T3.member_id JOIN major AS T4 ON T3.link_to_major = T4.major_id WHERE T1.event_name = 'Community Theater' AND T4.major_name = 'Interior Design'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.city = 'Georgetown' AND T2.state = 'South Carolina'
SELECT SUM(T1.amount) FROM income AS T1 JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T2.first_name = 'Grant' AND T2.last_name = 'Gilmour'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T2.amount > 40
SELECT SUM(T3.cost) AS total_expense FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget WHERE T1.event_name = 'Yearly Kickoff'
SELECT T4.first_name, T4.last_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget JOIN member AS T4 ON T3.link_to_member = T4.member_id WHERE T1.event_name = 'Yearly Kickoff'
SELECT T1.first_name, T1.last_name, T2.source FROM member AS T1 JOIN income AS T2 ON T1.member_id = T2.link_to_member ORDER BY T2.amount DESC LIMIT 1
SELECT T1.event_name FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event INNER JOIN expense AS T3 ON T2.event_status = 'Open' ORDER BY T3.cost ASC LIMIT 1
SELECT CAST(SUM(CASE WHEN T3.event_name = 'Yearly Kickoff' THEN T1.cost ELSE 0 END) AS REAL) * 100 / SUM(T1.cost) FROM expense AS T1 JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id JOIN event AS T3 ON T2.link_to_event = T3.event_id
SELECT CAST(SUM(CASE WHEN major_name = 'Finance' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN major_name = 'Physics' THEN 1 ELSE 0 END) AS ratio FROM major
SELECT source FROM income WHERE date_received BETWEEN '2019-09-01' AND '2019-09-30' GROUP BY source ORDER BY SUM(amount) DESC LIMIT 1
SELECT first_name, last_name, email FROM member WHERE `position` = 'Secretary'
SELECT COUNT(*) FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Physics Teaching'
SELECT COUNT(DISTINCT T2.link_to_member) FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'Community Theater' AND STRFTIME('%Y', T1.event_date) = '2019'
SELECT COUNT(T2.link_to_event), T4.major_name FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id INNER JOIN major AS T4 ON T1.link_to_major = T4.major_id WHERE T1.first_name = 'Luisa' AND T1.last_name = 'Guidi'
SELECT AVG(spent) FROM budget WHERE event_status = 'Closed' AND category = 'Food'
SELECT T2.event_name FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.category = 'Advertisement' ORDER BY T1.spent DESC LIMIT 1
SELECT COUNT(*) FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T1.first_name = 'Maya' AND T1.last_name = 'Mclean' AND T3.event_name = 'Women''s Soccer'
SELECT CAST(SUM(CASE WHEN type = 'Community Service' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(event_id) FROM event WHERE event_date BETWEEN '2019-01-01' AND '2019-12-31'
SELECT T1.cost FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T1.expense_description = 'Posters' AND T3.event_name = 'September Speaker'
SELECT t_shirt_size FROM member GROUP BY t_shirt_size ORDER BY COUNT(t_shirt_size) DESC LIMIT 1
SELECT T2.event_name FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.status = 'Closed' AND T1.remaining < 0 ORDER BY T1.remaining ASC LIMIT 1
SELECT T1.category, SUM(T2.cost) FROM budget AS T1 JOIN expense AS T2 ON T1.budget_id = T2.link_to_budget JOIN event AS T3 ON T1.link_to_event = T3.event_id WHERE T3.event_name = 'October Meeting'
SELECT T2.category, SUM(T2.amount) AS total_amount_budgeted FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'April Speaker' GROUP BY T2.category ORDER BY total_amount_budgeted ASC
SELECT amount FROM budget WHERE category = 'Food' ORDER BY amount DESC LIMIT 1
SELECT amount FROM budget WHERE category = 'Advertisement' ORDER BY amount DESC LIMIT 3
SELECT SUM(cost) FROM expense WHERE expense_description = 'Parking'
SELECT SUM(cost) FROM expense WHERE expense_date = '2019-08-20'
SELECT T1.first_name, T1.last_name, SUM(T2.cost) FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T2.link_to_member = 'rec4BLdZHS2Blfp4v'
SELECT T2.expense_description FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.first_name = 'Sacha' AND T1.last_name = 'Harrison'
SELECT T1.expense_description FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T2.t_shirt_size = 'X-Large'
SELECT DISTINCT T2.zip FROM expense AS T1 JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.cost < 50
SELECT T2.major_name FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Phillip' AND T1.last_name = 'Cullen'
SELECT T1.position FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Business'
SELECT COUNT(*) FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Business' AND T1.t_shirt_size = 'Medium'
SELECT T2.type FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.remaining > 30
SELECT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.location = 'MU 215'
SELECT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_date = '2020-03-24T12:00:00'
SELECT T2.major_name FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'Vice President'
SELECT CAST(SUM(CASE WHEN T2.major_name = 'Business' AND T1.position = 'Member' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.member_id) FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id
SELECT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.location = 'MU 215'
SELECT COUNT(income_id) FROM income WHERE amount = 50
SELECT COUNT(*) FROM member WHERE position = 'Member' AND t_shirt_size = 'X-Large'
SELECT COUNT(major_id) FROM major WHERE college = 'College of Agriculture and Applied Sciences' AND department = 'School of Applied Sciences, Technology and Education'
SELECT T1.last_name, T2.department, T2.college FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Environmental Engineering'
SELECT T1.category FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.location = 'MU 215' AND T2.type = 'Guest Speaker' AND T1.spent = 0
SELECT T3.city, T3.state FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major INNER JOIN zip_code AS T3 ON T2.zip = T3.zip_code WHERE T2.position = 'Member' AND T1.department = 'Electrical and Computer Engineering Department'
SELECT T1.event_name FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.type = 'Social' AND T3.position = 'Vice President' AND T1.location = '900 E. Washington St.'
SELECT T2.last_name, T2.position FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.expense_description = 'Pizza' AND T1.expense_date = '2019-09-10'
SELECT T1.last_name FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T3.event_name = 'Women''s Soccer' AND T1.position = 'Member'
SELECT CAST(COUNT(CASE WHEN T2.amount = 50 THEN 1 END) AS REAL) * 100 / COUNT(*) FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.t_shirt_size = 'Medium' AND T1.position = 'Member'
SELECT DISTINCT county FROM zip_code WHERE type = 'PO Box'
SELECT zip_code FROM zip_code WHERE type = 'PO Box' AND state = 'Puerto Rico' AND county = 'San Juan Municipio'
SELECT event_name FROM event WHERE type = 'Game' AND status = 'Closed' AND event_date BETWEEN '2019-03-15' AND '2020-03-20'
SELECT T2.link_to_event FROM expense AS T1 INNER JOIN attendance AS T2 ON T1.link_to_member = T2.link_to_member WHERE T1.cost > 50
SELECT T2.first_name, T2.last_name, T3.link_to_event FROM expense AS T1 JOIN attendance AS T3 ON T1.link_to_member = T3.link_to_member JOIN member AS T2 ON T3.link_to_member = T2.member_id WHERE T1.approved = 'true' AND T1.expense_date BETWEEN '2019-01-10' AND '2019-11-19'
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Katy' AND T2.major_id = 'rec1N0upiVLy5esTO'
SELECT T1.phone FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Business' AND T2.college = 'College of Agriculture and Applied Sciences'
SELECT T2.email FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.expense_date BETWEEN '2019-09-10' AND '2019-11-19' AND T1.cost > 20
SELECT COUNT(*) FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Education' AND T1.position = 'Member' AND T2.college = 'College of Education & Human Services'
SELECT CAST(SUM(CASE WHEN remaining < 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(budget_id) FROM budget
SELECT event_id, location, status FROM event WHERE event_date BETWEEN '2019-11-01' AND '2020-03-31'
SELECT expense_description FROM expense GROUP BY expense_description HAVING AVG(cost) > 50
SELECT first_name, last_name FROM member WHERE t_shirt_size = 'X-Large'
SELECT CAST(COUNT(CASE WHEN type = 'PO Box' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(zip_code) FROM zip_code
SELECT T1.event_name, T1.location FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T2.remaining > 0
SELECT T1.event_name, T1.event_date FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget WHERE T3.expense_description = 'Pizza' AND T3.cost > 50 AND T3.cost < 100
SELECT T1.first_name, T1.last_name, T2.major_name FROM member AS T1 JOIN expense AS T3 ON T1.member_id = T3.link_to_member JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T3.cost > 100
SELECT T4.city, T4.county FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event INNER JOIN income AS T3 ON T2.link_to_event = T3.link_to_member INNER JOIN zip_code AS T4 ON T1.location = T4.zip_code GROUP BY T4.city, T4.county HAVING COUNT(T3.income_id) > 40
SELECT T1.first_name, T1.last_name FROM member AS T1 JOIN expense AS T2 ON T1.member_id = T2.link_to_member GROUP BY T1.member_id, T1.first_name, T1.last_name ORDER BY SUM(T2.cost) DESC LIMIT 1
SELECT AVG(T2.cost) FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.position != 'Member'
SELECT T1.event_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event JOIN expense AS T3 ON T3.link_to_budget = T2.budget_id WHERE T2.category = 'Parking' AND T3.cost < ( SELECT AVG(cost) FROM expense WHERE link_to_budget IN ( SELECT budget_id FROM budget WHERE category = 'Parking' ) )
SELECT CAST(SUM(expense.cost) AS REAL) * 100 / COUNT(event.event_id) FROM event INNER JOIN budget ON event.event_id = budget.link_to_event INNER JOIN expense ON budget.budget_id = expense.link_to_budget WHERE event.type = 'Meeting'
SELECT expense_description FROM expense WHERE expense_description = 'Water, chips, cookies' ORDER BY cost DESC LIMIT 1
SELECT T1.first_name, T1.last_name FROM member AS T1 JOIN expense AS T2 ON T1.member_id = T2.link_to_member ORDER BY T2.cost DESC LIMIT 5
SELECT T1.first_name, T1.last_name, T1.phone FROM member AS T1 JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T2.cost > ( SELECT AVG(cost) FROM expense )
SELECT (CAST(SUM(CASE WHEN T2.state = 'New Jersey' THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(*) - (CAST(SUM(CASE WHEN T2.state = 'Vermont' THEN 1 ELSE 0 END) AS REAL) * 100) / COUNT(*) FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.position = 'Member'
SELECT T2.major_name, T2.department FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Garrett' AND T1.last_name = 'Gerke'
SELECT T2.first_name, T2.last_name, T1.cost FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.expense_description = 'Water, Veggie tray, supplies'
SELECT T1.last_name, T1.phone FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Elementary Education'
SELECT T2.category, T2.amount FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'January Speaker'
SELECT T1.event_name FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T2.category = 'Food'
SELECT T1.first_name, T1.last_name, T2.amount FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T2.date_received = '2019-09-09'
SELECT T2.category FROM expense AS T1 JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id WHERE T1.expense_description = 'Posters'
SELECT T1.first_name, T1.last_name, T2.college FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'Secretary'
SELECT SUM(T1.spent), T2.event_name FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.category = 'Speaker Gifts'
SELECT T2.city FROM member AS T1 JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Garrett' AND T1.last_name = 'Gerke'
SELECT T1.first_name, T1.last_name, T1.position FROM member AS T1 JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.city = 'Lincolnton' AND T2.state = 'North Carolina' AND T1.zip = 28092
SELECT COUNT(*) FROM gasstations WHERE Country = 'CZE' AND Segment = 'Premium'
SELECT CAST(COUNT(CASE WHEN Currency = 'EUR' THEN 1 ELSE NULL END) AS REAL) / COUNT(CASE WHEN Currency = 'CZK' THEN 1 ELSE NULL END) FROM customers
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'LAM' AND T2.Date LIKE '2012%' ORDER BY T2.Consumption ASC LIMIT 1
SELECT AVG(T2.Consumption) / 12 AS AverageMonthlyConsumption FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'SME' AND T2.Date LIKE '2013%'
SELECT T1.CustomerID FROM customers AS T1 JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'CZK' AND T2.Date BETWEEN '201101' AND '201112' ORDER BY T2.Consumption DESC LIMIT 1
SELECT COUNT(*) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'KAM' AND T2.Consumption < 30000 AND T2.`Date` LIKE '2012%'
SELECT SUM(CASE WHEN T2.Currency = 'CZK' THEN T1.Consumption ELSE 0 END) - SUM(CASE WHEN T2.Currency = 'EUR' THEN T1.Consumption ELSE 0 END) AS DifferenceInConsumption FROM yearmonth AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date LIKE '2012%'
SELECT T1.Date FROM yearmonth AS T1 JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Currency = 'EUR' GROUP BY T1.`Date` ORDER BY SUM(T1.Consumption) DESC LIMIT 1
SELECT T1.Segment FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID GROUP BY T1.Segment ORDER BY SUM(T2.Consumption) ASC LIMIT 1
SELECT SUBSTR(T1.`Date`, 1, 4) AS Year FROM yearmonth AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Currency = 'CZK' GROUP BY SUBSTR(T1.`Date`, 1, 4) ORDER BY SUM(T1.Consumption) DESC LIMIT 1
SELECT t1.Date FROM yearmonth AS t1 INNER JOIN customers AS t2 ON t1.CustomerID = t2.CustomerID WHERE t2.Segment = 'SME' AND SUBSTR(t1.Date, 1, 4) = '2013' GROUP BY t1.Date ORDER BY SUM(t1.Consumption) DESC LIMIT 1
SELECT (AVG(CASE WHEN Segment = 'SME' THEN Consumption ELSE NULL END) - AVG(CASE WHEN Segment = 'LAM' THEN Consumption ELSE NULL END)) AS Difference_SME_LAM, (AVG(CASE WHEN Segment = 'LAM' THEN Consumption ELSE NULL END) - AVG(CASE WHEN Segment = 'KAM' THEN Consumption ELSE NULL END)) AS Difference_LAM_KAM, (AVG(CASE WHEN Segment = 'KAM' THEN Consumption ELSE NULL END) - AVG(CASE WHEN Segment = 'SME' THEN Consumption ELSE NULL END)) AS Difference_KAM_SME FROM yearmonth INNER JOIN customers ON yearmonth.CustomerID = customers.CustomerID WHERE `Date` BETWEEN '201301' AND '201312' AND Currency = 'CZK'
SELECT T1.Segment, CAST(SUM(CASE WHEN T2.`Date` LIKE '2013%' THEN T2.Consumption ELSE 0 END) - SUM(CASE WHEN T2.`Date` LIKE '2012%' THEN T2.Consumption ELSE 0 END) AS REAL) * 100 / SUM(CASE WHEN T2.`Date` LIKE '2013%' THEN T2.Consumption ELSE 0 END) AS PercentageIncrease FROM customers AS T1 JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR' GROUP BY T1.Segment ORDER BY PercentageIncrease DESC LIMIT 1
SELECT SUM(Consumption) FROM yearmonth WHERE CustomerID = 6 AND `Date` BETWEEN '201308' AND '201311'
SELECT SUM(CASE WHEN Country = 'CZE' THEN 1 ELSE 0 END) - SUM(CASE WHEN Country = 'SVK' THEN 1 ELSE 0 END) AS Difference FROM gasstations WHERE Segment = 'Discount'
SELECT ( SELECT Consumption FROM yearmonth WHERE CustomerID = 7 AND `Date` = '201304' ) - ( SELECT Consumption FROM yearmonth WHERE CustomerID = 5 AND `Date` = '201304' ) AS Difference
SELECT SUM(CASE WHEN T1.Currency = 'CZK' THEN T2.Amount ELSE 0 END) - SUM(CASE WHEN T1.Currency = 'EUR' THEN T2.Amount ELSE 0 END) AS Difference FROM customers AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'SME'
SELECT T1.CustomerID FROM customers AS T1 JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'LAM' AND T1.Currency = 'EUR' AND T2.Date LIKE '201310' ORDER BY T2.Consumption DESC LIMIT 1
SELECT T1.CustomerID, T2.Consumption FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'KAM' ORDER BY T2.Consumption DESC LIMIT 1
SELECT SUM(y.Consumption) FROM customers AS x JOIN yearmonth AS y ON x.CustomerID = y.CustomerID WHERE x.Segment = 'KAM' AND y.Date BETWEEN '201305' AND '201305'
SELECT CAST(SUM(CASE WHEN T2.Consumption > 46.73 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'LAM'
SELECT Country, COUNT(CASE WHEN Segment = 'Value for money' THEN GasStationID END) FROM gasstations GROUP BY Country
SELECT CAST(COUNT(CASE WHEN Currency = 'EUR' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(CustomerID) FROM customers WHERE Segment = 'KAM'
SELECT CAST(SUM(CASE WHEN Consumption > 528.3 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM yearmonth WHERE `Date` = '201202'
SELECT (CAST(COUNT(CASE WHEN Segment = 'Premium' THEN GasStationID END) AS REAL) * 100 / COUNT(GasStationID)) FROM gasstations WHERE Country = 'SLO'
SELECT CustomerID FROM yearmonth WHERE `Date` LIKE '201309' ORDER BY Consumption DESC LIMIT 1
SELECT T1.Segment FROM customers AS T1 JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date LIKE '201309' GROUP BY T1.Segment ORDER BY SUM(T2.Consumption) ASC LIMIT 1
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.`Date` = '201206' AND T1.Segment = 'SME' ORDER BY T2.Consumption ASC LIMIT 1
SELECT MAX(Consumption) FROM yearmonth WHERE SUBSTR(`Date`, 1, 4) = '2012'
SELECT MAX(T2.Consumption) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR'
SELECT T1.Description FROM products AS T1 JOIN transactions_1k AS T2 ON T1.ProductID = T2.ProductID JOIN yearmonth AS T3 ON T2.CustomerID = T3.CustomerID WHERE SUBSTR(T3.Date, 1, 6) = '201309'
SELECT DISTINCT T3.Country FROM yearmonth AS T1 JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID JOIN gasstations AS T3 ON T2.GasStationID = T3.GasStationID WHERE T1.`Date` LIKE '201306%'
SELECT DISTINCT T3.ChainID FROM transactions_1k AS T1 JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID JOIN gasstations AS T3 ON T1.GasStationID = T3.GasStationID WHERE T2.Currency = 'EUR'
SELECT T2.Description FROM transactions_1k AS T1 INNER JOIN products AS T2 ON T1.ProductID = T2.ProductID INNER JOIN customers AS T3 ON T1.CustomerID = T3.CustomerID WHERE T3.Currency = 'EUR'
SELECT AVG(Price * Amount) FROM transactions_1k WHERE Date LIKE '2012-01-%'
SELECT COUNT(T1.CustomerID) FROM customers AS T1 JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR' AND T2.Consumption > 1000
SELECT T2.Description FROM transactions_1k AS T1 INNER JOIN products AS T2 ON T1.ProductID = T2.ProductID INNER JOIN gasstations AS T3 ON T1.GasStationID = T3.GasStationID WHERE T3.Country = 'CZE'
SELECT DISTINCT T1.Time FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T2.ChainID = 11
SELECT COUNT(T1.TransactionID)  FROM transactions_1k AS T1  INNER JOIN gasstations AS T2  ON T1.GasStationID = T2.GasStationID  WHERE T2.Country = 'CZE' AND T1.Price > 1000
SELECT COUNT(*) FROM transactions_1k AS T1 JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T2.Country = 'CZE' AND T1.Date > '2012-01-01'
SELECT AVG(transactions_1k.Price * transactions_1k.Amount) AS AverageTotalPrice FROM transactions_1k INNER JOIN gasstations ON transactions_1k.GasStationID = gasstations.GasStationID WHERE gasstations.Country = 'CZE'
SELECT AVG(T2.Price) FROM customers AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR'
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.`Date` = '2012-08-25' ORDER BY T2.Amount DESC LIMIT 1
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-25' ORDER BY T1.Time ASC LIMIT 1
SELECT T2.Currency FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.`Date` = '2012-08-24' AND T1.`Time` = '16:25:00'
SELECT T2.Segment FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '2012-08-23' AND T1.Time = '21:20:00'
SELECT COUNT(*) FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.`Date` = '2012-08-26' AND T1.`Time` BETWEEN '00:00:00' AND '13:00:00' AND T2.Currency = 'CZK'
SELECT Segment FROM customers WHERE CustomerID = (SELECT MIN(CustomerID) FROM customers)
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-24' AND T1.Time = '12:42:00'
SELECT ProductID FROM transactions_1k WHERE `Date` = '2012-08-23' AND `Time` = '21:20:00'
SELECT T2.`Date`, T2.Consumption as Expenses, SUM(CASE WHEN strftime('%m', T2.`Date`) = '01' THEN T2.Consumption ELSE 0 END) AS TotalExpensesInJanuary FROM transactions_1k AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.`Date` = '2012-08-24' AND T1.Amount = 124.05
SELECT COUNT(T1.TransactionID) AS NumberOfTransactions FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-26' AND T1.Time BETWEEN '08:00:00' AND '09:00:00' AND T2.Country = 'CZE'
SELECT T2.Currency FROM yearmonth AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date LIKE '201306' AND T1.Consumption = 214582.17
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.CardID = 667467
SELECT T1.Currency FROM customers AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date = '2012-08-24' AND T2.Price = 548.4
SELECT CAST(COUNT(CASE WHEN T1.Currency = 'EUR' THEN T1.CustomerID ELSE NULL END) AS REAL) * 100 / COUNT(T1.CustomerID) FROM customers AS T1 JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date = '2012-08-25'
SELECT (T1.Consumption - (SELECT Consumption FROM yearmonth WHERE CustomerID = T1.CustomerID AND `Date` LIKE '201308')) / T1.Consumption FROM yearmonth AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Amount = 634.8 AND T2.`Date` LIKE '2012-08-25'
SELECT T2.GasStationID FROM transactions_1k AS T1 JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID GROUP BY T2.GasStationID ORDER BY SUM(T1.Price * T1.Amount) DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN Segment = 'Premium' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM gasstations WHERE Country = 'SVK'
SELECT SUM(T1.Amount) FROM transactions_1k AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.CustomerID = 38508 AND T2.`Date` LIKE '201201'
SELECT T1.Description FROM products AS T1 INNER JOIN transactions_1k AS T2 ON T1.ProductID = T2.ProductID GROUP BY T1.ProductID ORDER BY SUM(T2.Amount) DESC LIMIT 5
SELECT t1.CustomerID, AVG(t1.Price / t1.Amount) AS average_price, t2.Currency FROM transactions_1k t1 JOIN customers t2 ON t1.CustomerID = t2.CustomerID GROUP BY t1.CustomerID ORDER BY SUM(t1.Price) DESC LIMIT 1
SELECT T3.Country FROM transactions_1k AS T1 JOIN products AS T2 ON T1.ProductID = T2.ProductID JOIN gasstations AS T3 ON T1.GasStationID = T3.GasStationID WHERE T2.ProductID = 2 ORDER BY T1.Price DESC LIMIT 1
SELECT T2.Consumption FROM transactions_1k AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date LIKE '201208' AND T1.ProductID = 5 AND (T1.Price / T1.Amount) > 29.00