SELECT MAX(`Free Meal Count (K-12)` / `Enrollment (K-12)`) AS HighestEligibleFreeRate FROM frpm WHERE `County Name` = 'Alameda'
SELECT (`Free Meal Count (Ages 5-17)` / `Enrollment (Ages 5-17)`) AS EligibleFreeRate FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode WHERE schools.SOCType = 'Continuation School' ORDER BY EligibleFreeRate ASC LIMIT 3
SELECT T2.Zip FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 AND T1.`District Name` = 'Fresno County Office of Education'
SELECT T1.MailStreet FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode ORDER BY T2.`FRPM Count (K-12)` DESC LIMIT 1
SELECT T2.Phone FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 AND T2.FundingType = 'Directly funded' AND T2.OpenDate > '2000-01-01'
SELECT COUNT(DISTINCT T1.CDSCode) FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.Virtual = 'F' AND T2.AvgScrMath > 400
SELECT T2.School FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.NumTstTakr > 500 AND T2.Magnet = 1
SELECT s.Phone FROM satscores ss JOIN schools s ON ss.cds = s.CDSCode ORDER BY ss.NumGE1500 DESC LIMIT 1
SELECT NumTstTakr FROM (SELECT CDSCode FROM frpm ORDER BY `FRPM Count (K-12)` DESC LIMIT 1) AS highest_frpm_school JOIN satscores ON highest_frpm_school.CDSCode = satscores.cds
SELECT COUNT(*) FROM satscores ss JOIN schools s ON ss.cds = s.CDSCode WHERE ss.AvgScrMath > 560 AND s.FundingType = 'Directly funded'
SELECT T2.`FRPM Count (Ages 5-17)` FROM satscores AS T1 INNER JOIN frpm AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrRead DESC LIMIT 1
SELECT CDSCode FROM frpm WHERE `Enrollment (K-12)` + `Enrollment (Ages 5-17)` > 500
SELECT MAX(f."Free Meal Count (Ages 5-17)" / f."Enrollment (Ages 5-17)") AS max_eligible_free_rate FROM frpm f JOIN satscores s ON f.CDSCode = s.cds WHERE s.NumGE1500 / s.NumTstTakr > 0.3
SELECT s.Phone FROM satscores ss INNER JOIN schools s ON ss.cds = s.CDSCode ORDER BY (ss.NumGE1500 / ss.NumTstTakr) DESC LIMIT 3
SELECT s.NCESSchool FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode ORDER BY f.`Enrollment (Ages 5-17)` DESC LIMIT 5
SELECT dname FROM satscores JOIN schools ON satscores.cds = schools.CDSCode WHERE schools.StatusType = 'Active' GROUP BY dname ORDER BY AVG(satscores.AvgScrRead) DESC LIMIT 1
SELECT COUNT(*) FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds WHERE s.StatusType = 'Merged' AND s.County = 'Alameda' AND ss.NumTstTakr < 100
SELECT T2.CharterNum FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T1.AvgScrWrite > 499 AND T2.CharterNum IS NOT NULL ORDER BY T1.AvgScrWrite DESC
SELECT COUNT(*) FROM schools JOIN satscores ON schools.CDSCode = satscores.cds WHERE schools.County = 'Fresno' AND schools.FundingType = 'Directly funded' AND satscores.NumTstTakr <= 250
SELECT T2.Phone FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrMath DESC LIMIT 1
SELECT COUNT(s.CDSCode)  FROM frpm f  INNER JOIN schools s ON f.CDSCode = s.CDSCode  WHERE s.County = 'Amador' AND f.`Low Grade` = '9' AND f.`High Grade` = '12'
SELECT COUNT(*) FROM frpm WHERE `County Name` = 'Los Angeles' AND `Free Meal Count (K-12)` > 500 AND `FRPM Count (K-12)` < 700
SELECT s.School FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds WHERE s.County = 'Contra Costa' ORDER BY ss.NumTstTakr DESC LIMIT 1
SELECT s.School, s.Street FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE f.`Enrollment (K-12)` - f.`Enrollment (Ages 5-17)` > 30
SELECT T1.`School Name` FROM frpm AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.`Percent (%) Eligible Free (K-12)` > 0.1 AND T2.NumGE1500 > 0
SELECT DISTINCT s.FundingType FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds WHERE s.County = 'Riverside' GROUP BY s.CDSCode HAVING AVG(ss.AvgScrMath) > 400
SELECT T1.School, T1.Street, T1.City, T1.State, T1.Zip FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.County = 'Monterey' AND T1.SOCType = 'High Schools (Public)' AND T2.`FRPM Count (Ages 5-17)` > 800
SELECT s.School, ss.AvgScrWrite, s.Phone FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds WHERE s.OpenDate > '1991-12-31' OR s.ClosedDate < '2000-01-01'
SELECT s.School, s.DOCType FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE f.[Enrollment (K-12)] - f.[Enrollment (Ages 5-17)] > ( SELECT AVG(f.[Enrollment (K-12)] - f.[Enrollment (Ages 5-17)]) FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.FundingType = 'Locally funded' ) AND s.FundingType = 'Locally funded'
SELECT s.OpenDate FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE f.`School Type` = 'K-12 Schools (Public)' ORDER BY f.`Enrollment (K-12)` DESC LIMIT 1
SELECT T1.City FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds ORDER BY T2.enroll12 ASC LIMIT 5
SELECT `Free Meal Count (K-12)` / `Enrollment (K-12)` AS EligibleFreeRate FROM frpm ORDER BY `Enrollment (K-12)` DESC LIMIT 9, 2
SELECT `FRPM Count (K-12)` / `Enrollment (K-12)` AS `Eligible Free or Reduced Price Meal Rate` FROM ( SELECT * FROM schools JOIN frpm ON schools.CDSCode = frpm.CDSCode WHERE schools.SOC = 66 AND frpm.`Enrollment (K-12)` > 0 ORDER BY frpm.`FRPM Count (K-12)` DESC LIMIT 5 ) AS top_schools
SELECT T2.Website, T2.School FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1."Free Meal Count (Ages 5-17)" BETWEEN 1900 AND 2000
SELECT (frpm."Free Meal Count (Ages 5-17)" / frpm."Enrollment (Ages 5-17)") AS free_rate FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode WHERE schools.AdmFName1 = 'Kacey' AND schools.AdmLName1 = 'Gibson'
SELECT T2.AdmEmail1 FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`Charter School (Y/N)` = 1 ORDER BY T1.`Enrollment (K-12)` ASC LIMIT 1
SELECT AdmFName1, AdmLName1, AdmFName2, AdmLName2, AdmFName3, AdmLName3 FROM schools JOIN satscores ON schools.CDSCode = satscores.cds WHERE satscores.NumGE1500 = (SELECT MAX(NumGE1500) FROM satscores)
SELECT s.Street, s.City, s.Zip, s.State FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds ORDER BY (CAST(ss.NumGE1500 AS REAL) / ss.NumTstTakr) ASC LIMIT 1
SELECT DISTINCT T1.Website FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds WHERE T1.County = 'Los Angeles' AND T2.NumTstTakr BETWEEN 2000 AND 3000
SELECT AVG(s.NumTstTakr) FROM schools sch JOIN satscores s ON sch.CDSCode = s.cds WHERE sch.County = 'Fresno' AND sch.OpenDate BETWEEN '1980-01-01' AND '1980-12-31'
SELECT t2.Phone FROM satscores AS t1 INNER JOIN schools AS t2 ON t1.dname = t2.District AND t1.sname = t2.School WHERE t1.dname = 'Fresno Unified' ORDER BY t1.AvgScrRead ASC LIMIT 1
SELECT School FROM ( SELECT *, ROW_NUMBER() OVER (PARTITION BY County ORDER BY AvgScrRead DESC) as Rank FROM schools JOIN satscores ON schools.CDSCode = satscores.cds WHERE Virtual = 'F' ) ranked WHERE ranked.Rank <= 5
SELECT T2.EdOpsName FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrMath DESC LIMIT 1
SELECT AvgScrMath, T2.County FROM satscores AS T1 JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY (AvgScrMath + AvgScrRead + AvgScrWrite) / 3 ASC LIMIT 1
SELECT s.AvgScrWrite, sc.City FROM satscores s JOIN schools sc ON s.cds = sc.CDSCode ORDER BY s.NumGE1500 DESC LIMIT 1
SELECT s.School, AVG(t.AvgScrWrite) AS AverageWritingScore FROM schools s JOIN satscores t ON s.CDSCode = t.cds WHERE s.AdmFName1 = 'Ricci' AND s.AdmLName1 = 'Ulrich' GROUP BY s.School
SELECT s.School FROM schools s JOIN satscores sa ON s.CDSCode = sa.cds WHERE s.DOC = '31' AND s.GSserved = 'K-12' ORDER BY sa.enroll12 DESC LIMIT 1
SELECT CAST(COUNT(*) AS REAL) / 12 AS monthly_average FROM schools WHERE County = 'Alameda' AND DOC = '52' AND strftime('%Y', OpenDate) = '1980'
SELECT CAST(SUM(CASE WHEN DOC = '54' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN DOC = '52' THEN 1 ELSE 0 END) AS ratio FROM schools WHERE StatusType = 'Merged' AND County = 'Orange'
SELECT s.School, s.ClosedDate FROM schools s JOIN ( SELECT County, COUNT(*) AS ClosedCount FROM schools WHERE StatusType = 'Closed' GROUP BY County ORDER BY ClosedCount DESC LIMIT 1 ) AS ClosedCounty ON s.County = ClosedCounty.County WHERE s.StatusType = 'Closed'
SELECT T1.Street, T1.School FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds ORDER BY T2.AvgScrMath DESC LIMIT 6, 1
SELECT T2.MailStreet, T2.School FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode ORDER BY T1.AvgScrRead ASC LIMIT 1
SELECT COUNT(*) FROM satscores s JOIN schools sc ON s.cds = sc.CDSCode WHERE sc.MailCity = 'Lakeport' AND (s.AvgScrRead + s.AvgScrMath + s.AvgScrWrite) >= 1500
SELECT SUM(NumTstTakr) FROM schools JOIN satscores ON schools.CDSCode = satscores.cds WHERE schools.MailCity = 'Fresno'
SELECT School, MailZip FROM schools WHERE (AdmFName1 = 'Avetik' AND AdmLName1 = 'Atoian') OR (AdmFName2 = 'Avetik' AND AdmLName2 = 'Atoian') OR (AdmFName3 = 'Avetik' AND AdmLName3 = 'Atoian')
SELECT CAST(COUNT(CASE WHEN County = 'Colusa' THEN 1 END) AS REAL) / COUNT(CASE WHEN County = 'Humboldt' THEN 1 END) AS ratio FROM schools WHERE MailState = 'CA'
SELECT COUNT(*) FROM schools WHERE StatusType = 'Active' AND City = 'San Joaquin' AND MailState = 'CA'
SELECT s.Phone, s.Ext FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds ORDER BY ss.AvgScrWrite DESC LIMIT 332, 1
SELECT Phone, Ext, School FROM schools WHERE Zip = '95203-3704'
SELECT Website FROM schools WHERE (AdmFName1 = 'Mike' AND AdmLName1 = 'Larson') OR (AdmFName2 = 'Mike' AND AdmLName2 = 'Larson') OR (AdmFName3 = 'Mike' AND AdmLName3 = 'Larson') OR (AdmFName1 = 'Dante' AND AdmLName1 = 'Alvarez') OR (AdmFName2 = 'Dante' AND AdmLName2 = 'Alvarez') OR (AdmFName3 = 'Dante' AND AdmLName3 = 'Alvarez')
SELECT Website FROM schools WHERE Virtual = 'P' AND Charter = 1 AND County = 'San Joaquin'
SELECT COUNT(CDSCode) FROM schools WHERE Charter = 1 AND City = 'Hickman' AND DOC = '52'
SELECT COUNT(s.CDSCode) FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.Charter = 0 AND s.County = 'Los Angeles' AND (f.`Free Meal Count (K-12)` / f.`Enrollment (K-12)`) * 100 < 0.18
SELECT AdmFName1, AdmLName1, AdmFName2, AdmLName2, AdmFName3, AdmLName3, School, City FROM schools WHERE Charter = 1 AND CharterNum = '00D2'
SELECT COUNT(*) FROM schools WHERE MailCity = 'Hickman' AND CharterNum = '00D4'
SELECT (COUNT(CASE WHEN FundingType = 'Locally funded' THEN 1 END) * 100.0 / COUNT(*)) AS RatioPercent FROM schools WHERE County = 'Santa Clara'
SELECT COUNT(*) FROM schools WHERE FundingType = 'Directly funded' AND OpenDate BETWEEN '2000-01-01' AND '2005-12-31' AND County = 'Stanislaus'
SELECT COUNT(*) FROM schools WHERE County = 'San Francisco' AND DOCType = 'Community College District' AND STRFTIME('%Y', ClosedDate) = '1989'
SELECT County FROM schools WHERE SOC = '11' AND ClosedDate BETWEEN '1980-01-01' AND '1989-12-31' GROUP BY County ORDER BY COUNT(*) DESC LIMIT 1
SELECT NCESDist FROM schools WHERE SOC = '31'
SELECT COUNT(CDSCode) FROM schools WHERE StatusType IN ('Active', 'Closed') AND SOCType = 'District Community Day Schools' AND County = 'Alpine'
SELECT District FROM schools WHERE City = 'Fresno' AND Magnet = 0
SELECT frpm."Enrollment (Ages 5-17)" FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode WHERE schools.EDOpsCode = 'SSS' AND schools.City = 'Fremont' AND frpm."Academic Year" = '2014-2015'
SELECT T2.`FRPM Count (Ages 5-17)` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.EdOpsName = 'Youth Authority School' AND T1.MailStreet = 'PO Box 1040'
SELECT SUBSTR(GSoffered, 1, INSTR(GSoffered, '-') - 1) AS LowestGrade FROM schools WHERE EdOpsCode = 'SPECON' AND NCESDist = '0613360'
SELECT T1.EILName, T1.School FROM schools AS T1 JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.`County Code` = '37' AND T2.`NSLP Provision Status` = 'Breakfast Provision 2'
SELECT T2.City FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`County Name` = 'Merced' AND T1.`Low Grade` = '9' AND T1.`High Grade` = '12' AND T1.`NSLP Provision Status` = 'Lunch Provision 2' AND T2.EILCode = 'HS'
SELECT s.School, (f."FRPM Count (Ages 5-17)" / CAST(f."Enrollment (Ages 5-17)" AS REAL)) * 100 AS Percent_Eligible_FRPM FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.GSserved = 'K-9' AND s.County = 'Los Angeles'
SELECT GSserved FROM schools WHERE City = 'Adelanto' GROUP BY GSserved ORDER BY COUNT(GSserved) DESC LIMIT 1
SELECT County, COUNT(*) AS NumberOfSchools FROM schools WHERE County IN ('San Diego', 'Santa Barbara') AND Virtual = 'F' GROUP BY County ORDER BY NumberOfSchools DESC LIMIT 1
SELECT SOCType, School, Latitude FROM schools ORDER BY Latitude DESC LIMIT 1
SELECT s.City, f."Low Grade", s.School FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.State = 'CA' ORDER BY s.Latitude ASC LIMIT 1
SELECT GSoffered FROM schools ORDER BY ABS(Longitude) DESC LIMIT 1
SELECT s.City, COUNT(s.CDSCode) AS NumberOfSchools FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.Magnet = 1 AND s.GSoffered = 'K-8' AND f.`NSLP Provision Status` = 'Multiple Provision Types' GROUP BY s.City
SELECT AdmFName, District FROM ( SELECT AdmFName1 AS AdmFName, District FROM schools WHERE AdmFName1 IS NOT NULL UNION ALL SELECT AdmFName2 AS AdmFName, District FROM schools WHERE AdmFName2 IS NOT NULL UNION ALL SELECT AdmFName3 AS AdmFName, District FROM schools WHERE AdmFName3 IS NOT NULL ) AS admin_names GROUP BY AdmFName, District ORDER BY COUNT(*) DESC LIMIT 2
SELECT (frpm.`Free Meal Count (K-12)` / frpm.`Enrollment (K-12)`) * 100 AS percent_eligible_free_k12, frpm.`District Code` FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode WHERE schools.AdmFName1 = 'Alusine'
SELECT AdmLName1, District, County, School FROM schools WHERE CharterNum = '40'
SELECT AdmEmail1, AdmEmail2, AdmEmail3 FROM schools WHERE County = 'San Bernardino' AND District = 'San Bernardino City Unified' AND OpenDate BETWEEN '2009-01-01' AND '2010-12-31' AND SOC = '62' AND DOC = '54'
SELECT s.AdmEmail1, ss.sname FROM schools s JOIN satscores ss ON s.CDSCode = ss.cds WHERE ss.cds = ( SELECT cds FROM satscores ORDER BY NumGE1500 DESC LIMIT 1 )
SELECT COUNT(a.account_id) FROM account a JOIN district d ON a.district_id = d.district_id WHERE a.frequency = 'POPLATEK PO OBRATU' AND d.A3 = 'east Bohemia'
SELECT COUNT(DISTINCT a.account_id) FROM account a JOIN district d ON a.district_id = d.district_id JOIN loan l ON a.account_id = l.account_id WHERE d.A3 = 'Prague'
SELECT AVG(A12) AS avg_1995, AVG(A13) AS avg_1996 FROM district
SELECT COUNT(district_id) FROM district WHERE A11 > 6000 AND A11 < 10000
SELECT COUNT(*) FROM client JOIN district ON client.district_id = district.district_id WHERE client.gender = 'M' AND district.A3 = 'north Bohemia' AND district.A11 > 8000
SELECT d.account_id, (SELECT MAX(A11) - MIN(A11) FROM district) AS salary_gap FROM client c JOIN disp d ON c.client_id = d.client_id WHERE c.gender = 'F' ORDER BY c.birth_date ASC LIMIT 1
SELECT a.account_id FROM account a JOIN client c ON a.account_id = c.client_id JOIN district d ON c.district_id = d.district_id WHERE d.A11 = (SELECT MAX(A11) FROM district) ORDER BY c.birth_date DESC LIMIT 1
SELECT COUNT(*) FROM account a JOIN disp d ON a.account_id = d.account_id WHERE a.frequency = 'POPLATEK TYDNE' AND d.type = 'OWNER'
SELECT T1.client_id FROM disp AS T1 JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T2.frequency = 'POPLATEK PO OBRATU' AND T1.type = 'DISPONENT'
SELECT a.account_id FROM account a JOIN loan l ON a.account_id = l.account_id WHERE l.date LIKE '1997%' AND a.frequency = 'POPLATEK TYDNE' ORDER BY l.amount ASC LIMIT 1
SELECT T1.account_id FROM account AS T1 INNER JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T2.duration > 12 AND T1.`date` >= '1993-01-01' AND T1.`date` <= '1993-12-31' ORDER BY T2.amount DESC LIMIT 1
SELECT COUNT(*) FROM client AS c JOIN district AS d ON c.district_id = d.district_id WHERE c.gender = 'F' AND c.birth_date < '1950-01-01' AND d.A2 = 'Sokolov'
SELECT account_id FROM trans WHERE date = ( SELECT MIN(date) FROM trans WHERE date BETWEEN '1995-01-01' AND '1995-12-31' )
SELECT DISTINCT account.account_id FROM account JOIN trans ON account.account_id = trans.account_id WHERE account.date < '1997-01-01' GROUP BY account.account_id HAVING SUM(trans.amount) > 3000
SELECT T2.client_id FROM card AS T1 INNER JOIN disp AS T2 ON T1.disp_id = T2.disp_id WHERE T1.issued = '1994-03-03'
SELECT a.date FROM account a JOIN trans t ON a.account_id = t.account_id WHERE t.amount = 840 AND t.date = '1998-10-14'
SELECT DISTINCT T2.district_id FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.`date` = '1994-08-25'
SELECT MAX(trans.amount) AS biggest_transaction_amount FROM card JOIN disp ON card.disp_id = disp.disp_id JOIN trans ON disp.account_id = trans.account_id WHERE card.issued = '1996-10-21'
SELECT c.gender FROM client c JOIN account a ON c.client_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE d.district_id = (SELECT district_id FROM district ORDER BY A11 DESC LIMIT 1) ORDER BY c.birth_date LIMIT 1
SELECT t.amount FROM loan l JOIN account a ON l.account_id = a.account_id JOIN trans t ON a.account_id = t.account_id WHERE l.amount = (SELECT MAX(amount) FROM loan) ORDER BY t.date LIMIT 1
SELECT COUNT(*) FROM client c JOIN account a ON c.client_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE d.A2 = 'Jesenik' AND c.gender = 'F'
SELECT d.disp_id FROM trans t JOIN disp d ON t.account_id = d.account_id WHERE t.amount = 5100 AND t.date = '1998-09-02'
SELECT COUNT(*) FROM account a JOIN district d ON a.district_id = d.district_id WHERE d.A2 = 'Litomerice' AND strftime('%Y', a.date) = '1996'
SELECT d.A2 FROM client c JOIN disp dp ON c.client_id = dp.client_id JOIN account a ON dp.account_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE c.gender = 'F' AND c.birth_date = '1976-01-29'
SELECT T3.birth_date FROM loan AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id INNER JOIN client AS T3 ON T2.client_id = T3.client_id WHERE T1.amount = 98832 AND T1.`date` = '1996-01-03'
SELECT account_id FROM account WHERE district_id IN (SELECT district_id FROM district WHERE A3 = 'Prague') ORDER BY date LIMIT 1
SELECT (COUNT(CASE WHEN c.gender = 'M' THEN 1 END) * 100.0 / COUNT(*)) AS male_percentage FROM client c JOIN district d ON c.district_id = d.district_id WHERE d.A3 = 'south Bohemia' ORDER BY d.A4 DESC LIMIT 1
SELECT (t2.balance - t1.balance) / t1.balance * 100 AS increase_rate FROM trans t1 JOIN trans t2 ON t1.account_id = t2.account_id JOIN loan l ON t1.account_id = l.account_id JOIN client c ON l.account_id = c.client_id WHERE l.`date` = '1993-07-05' AND t1.`date` = '1993-03-22' AND t2.`date` = '1998-12-27' ORDER BY l.`date` LIMIT 1
SELECT CAST(SUM(IIF(status = 'A', amount, 0)) AS REAL) * 100 / SUM(amount) AS percentage FROM loan
SELECT (SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage_running FROM loan WHERE amount < 100000
SELECT T1.account_id, T2.A2, T2.A3 FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.frequency = 'POPLATEK PO OBRATU' AND STRFTIME('%Y', T1.date) = '1993'
SELECT T1.account_id, T1.frequency FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A3 = 'east Bohemia' AND STRFTIME('%Y', T1.date) BETWEEN '1995' AND '2000'
SELECT a.account_id, a.date FROM account a INNER JOIN district d ON a.district_id = d.district_id WHERE d.A2 = 'Prachatice'
SELECT T3.A2, T3.A3 FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.loan_id = 4990
SELECT l.account_id, d.A2 AS district, d.A3 AS region FROM loan l JOIN account a ON l.account_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE l.amount > 300000
SELECT T1.loan_id, T3.A3, T3.A11 FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.duration = 60
SELECT d.A2 AS district, ((d.A13 - d.A12) / d.A12) * 100 AS unemployment_rate_increment FROM district d JOIN account a ON d.district_id = a.district_id JOIN loan l ON a.account_id = l.account_id WHERE l.status = 'D'
SELECT CAST(SUM(CASE WHEN T2.A2 = 'Decin' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE STRFTIME('%Y', T1.date) = '1993'
SELECT account_id FROM account WHERE frequency = 'POPLATEK MESICNE'
SELECT d.A2 FROM district d JOIN account a ON d.district_id = a.district_id JOIN disp disp ON a.account_id = disp.account_id JOIN client c ON disp.client_id = c.client_id WHERE c.gender = 'F' GROUP BY d.district_id ORDER BY COUNT(c.client_id) DESC LIMIT 9
SELECT d.A2 AS district_name, SUM(t.amount) AS total_withdrawals FROM trans t JOIN account a ON t.account_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE t.type = 'VYDAJ' AND t.operation != 'PRIJEM' AND t.date LIKE '1996-01%' GROUP BY d.A2 ORDER BY total_withdrawals DESC LIMIT 10
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id LEFT JOIN card AS T3 ON T1.account_id = T3.disp_id WHERE T2.A3 = 'south bohemia' AND T3.card_id IS NULL
SELECT d.A3 FROM loan l JOIN account a ON l.account_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE l.status IN ('C', 'D') GROUP BY d.A3 ORDER BY COUNT(l.loan_id) DESC LIMIT 1
SELECT AVG(loan.amount) FROM client JOIN disp ON client.client_id = disp.client_id JOIN loan ON disp.account_id = loan.account_id WHERE client.gender = 'M'
SELECT district_id, A2 FROM district ORDER BY A13 DESC
SELECT COUNT(*) FROM account WHERE district_id = (SELECT district_id FROM district ORDER BY A16 DESC LIMIT 1)
SELECT COUNT(T.account_id) FROM ( SELECT T1.account_id FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.type = 'VYDAJ' AND T1.operation = 'VYBER KARTOU' AND T1.balance < 0 AND T2.frequency = 'POPLATEK MESICNE' GROUP BY T1.account_id ) T
SELECT COUNT(*) FROM loan l JOIN account a ON l.account_id = a.account_id WHERE a.frequency = 'POPLATEK MESICNE' AND l.amount >= 250000 AND l.date BETWEEN '1995-01-01' AND '1997-12-31'
SELECT COUNT(*) FROM loan AS l JOIN account AS a ON l.account_id = a.account_id WHERE l.status IN ('C', 'D') AND a.district_id = 1
SELECT COUNT(*) FROM client c JOIN district d ON c.district_id = d.district_id WHERE c.gender = 'M' AND d.district_id IN ( SELECT district_id FROM district ORDER BY A15 DESC LIMIT 1 OFFSET 1 )
SELECT COUNT(*) FROM card JOIN disp ON card.disp_id = disp.disp_id WHERE card.type = 'gold' AND disp.type = 'OWNER'
SELECT COUNT(*) FROM account a JOIN district d ON a.district_id = d.district_id WHERE d.A2 = 'Pisek'
SELECT DISTINCT T2.district_id FROM trans AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE STRFTIME('%Y', T1.`date`) = '1997' AND T1.amount > 10000
SELECT DISTINCT T2.account_id FROM district AS T1 INNER JOIN account AS T2 ON T1.district_id = T2.district_id INNER JOIN `order` AS T3 ON T2.account_id = T3.account_id WHERE T1.A2 = 'Pisek' AND T3.k_symbol = 'SIPO'
SELECT T2.account_id FROM card AS T1 INNER JOIN disp AS T2 ON T1.disp_id = T2.disp_id WHERE T1.type = 'gold'
SELECT AVG(amount) FROM trans WHERE operation = 'VYBER KARTOU' AND STRFTIME('%Y', date) = '2021'
SELECT account_id FROM trans WHERE trans_id IN ( SELECT trans_id FROM trans WHERE STRFTIME('%Y', date) = '1998' AND operation = 'VYBER KARTOU' AND amount < ( SELECT AVG(amount) FROM trans WHERE STRFTIME('%Y', date) = '1998' AND operation = 'VYBER KARTOU' ) )
SELECT T1.client_id FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN account AS T3 ON T2.account_id = T3.account_id INNER JOIN card AS T4 ON T2.disp_id = T4.disp_id INNER JOIN loan AS T5 ON T3.account_id = T5.account_id WHERE T1.gender = 'F'
SELECT COUNT(*) FROM client JOIN district ON client.district_id = district.district_id WHERE client.gender = 'F' AND district.A3 = 'south Bohemia'
SELECT a.account_id FROM account a JOIN disp d ON a.account_id = d.account_id JOIN district di ON a.district_id = di.district_id WHERE di.A2 = 'Tabor' AND d.type = 'OWNER'
SELECT t1.type FROM disp AS t1 JOIN account AS t2 ON t1.account_id = t2.account_id JOIN district AS t3 ON t2.district_id = t3.district_id WHERE t1.type != 'OWNER' AND t3.A11 > 8000 AND t3.A11 <= 9000
SELECT COUNT(DISTINCT a.account_id)  FROM district d JOIN account a ON d.district_id = a.district_id JOIN trans t ON a.account_id = t.account_id WHERE d.A3 = 'north Bohemia' AND t.bank = 'AB'
SELECT DISTINCT T2.A2 FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id INNER JOIN trans AS T3 ON T1.account_id = T3.account_id WHERE T3.type = 'VYDAJ'
SELECT AVG(d.A15) AS average_number_of_crimes FROM district d JOIN account a ON d.district_id = a.district_id WHERE d.A15 > 4000 AND STRFTIME('%Y', a.date) >= '1997'
SELECT COUNT(c.card_id) FROM card c JOIN disp d ON c.disp_id = d.disp_id JOIN account a ON d.account_id = a.account_id WHERE d.type = 'OWNER' AND c.type = 'classic'
SELECT COUNT(*) FROM client c JOIN district d ON c.district_id = d.district_id WHERE c.gender = 'M' AND d.A2 = 'Hl.m. Praha'
SELECT CAST(SUM(CASE WHEN type = 'gold' AND STRFTIME('%Y', issued) < '1998' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percent_gold_before_1998 FROM card
SELECT c.client_id FROM client c JOIN disp d ON c.client_id = d.client_id JOIN account a ON d.account_id = a.account_id JOIN loan l ON a.account_id = l.account_id ORDER BY l.amount DESC LIMIT 1
SELECT T2.A15 FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.account_id = 532
SELECT T1.district_id FROM account AS T1 INNER JOIN `order` AS T2 ON T1.account_id = T2.account_id WHERE T2.order_id = 33333
SELECT T2.trans_id FROM disp AS T1 INNER JOIN trans AS T2 ON T1.account_id = T2.account_id WHERE T1.client_id = 3356 AND T2.operation = 'VYBER'
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN loan AS T2 ON T1.account_id = T2.account_id WHERE T1.frequency = 'POPLATEK TYDNE' AND T2.amount < 200000
SELECT c.type FROM card c JOIN disp d ON c.disp_id = d.disp_id WHERE d.client_id = 13539
SELECT T2.A3 FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.client_id = 3541
SELECT d.district_id FROM loan l JOIN account a ON l.account_id = a.account_id JOIN district d ON a.district_id = d.district_id WHERE l.status = 'A' GROUP BY d.district_id ORDER BY COUNT(l.loan_id) DESC LIMIT 1
SELECT T2.client_id FROM disp AS T1 INNER JOIN client AS T2 ON T1.client_id = T2.client_id INNER JOIN `order` AS T3 ON T1.account_id = T3.account_id WHERE T3.order_id = 32423
SELECT t.* FROM trans t JOIN account a ON t.account_id = a.account_id WHERE a.district_id = 5
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A2 = 'Jesenik'
SELECT T2.client_id FROM card AS T1 INNER JOIN disp AS T2 ON T1.disp_id = T2.disp_id WHERE T1.type = 'junior' AND T1.issued >= '1997-01-01'
SELECT CAST(SUM(CASE WHEN c.gender = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS women_percentage FROM district d JOIN client c ON d.district_id = c.district_id JOIN disp disp ON c.client_id = disp.client_id JOIN account a ON disp.account_id = a.account_id WHERE d.A11 > 10000
SELECT CAST(SUM(CASE WHEN strftime('%Y', l.date) = '1997' THEN l.amount ELSE 0 END) - SUM(CASE WHEN strftime('%Y', l.date) = '1996' THEN l.amount ELSE 0 END) AS REAL) * 100 / SUM(CASE WHEN strftime('%Y', l.date) = '1996' THEN l.amount ELSE 0 END) AS growth_rate FROM loan l JOIN account a ON l.account_id = a.account_id JOIN disp d ON a.account_id = d.account_id JOIN client c ON d.client_id = c.client_id WHERE c.gender = 'M'
SELECT COUNT(*) FROM trans WHERE operation = 'VYBER KARTOU' AND date > '1995-12-31'
SELECT SUM(CASE WHEN A3 = 'north Bohemia' THEN A16 ELSE 0 END) - SUM(CASE WHEN A3 = 'east Bohemia' THEN A16 ELSE 0 END) AS difference FROM district
SELECT COUNT(disp_id) FROM disp WHERE account_id BETWEEN 1 AND 10 AND type IN ('OWNER', 'DISPONENT')
SELECT k_symbol FROM trans WHERE account_id = 3 AND amount = 3539
SELECT strftime('%Y', birth_date) FROM client WHERE client_id = 130
SELECT COUNT(T1.account_id) FROM disp AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.type = 'OWNER' AND T2.frequency = 'POPLATEK PO OBRATU'
SELECT SUM(t1.amount) AS total_debt, MAX(t1.status) AS payment_status FROM loan AS t1 INNER JOIN account AS t2 ON t1.account_id = t2.account_id INNER JOIN disp AS t3 ON t2.account_id = t3.account_id WHERE t3.client_id = 992
SELECT T3.balance, T1.gender FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN trans AS T3 ON T2.account_id = T3.account_id WHERE T1.client_id = 4 AND T3.trans_id = 851
SELECT c.type FROM card c JOIN disp d ON c.disp_id = d.disp_id WHERE d.client_id = 9
SELECT SUM(t.amount) AS total_amount_paid FROM trans t JOIN disp d ON t.account_id = d.account_id JOIN client c ON d.client_id = c.client_id WHERE c.client_id = 617 AND t.date >= '1998-01-01' AND t.date < '1999-01-01'
SELECT T1.client_id FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.birth_date BETWEEN '1983-01-01' AND '1987-12-31' AND T2.A3 = 'east Bohemia'
SELECT T1.client_id FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN loan AS T3 ON T2.account_id = T3.account_id WHERE T1.gender = 'F' ORDER BY T3.amount DESC LIMIT 3
SELECT COUNT(DISTINCT c.client_id) FROM client c JOIN disp d ON c.client_id = d.client_id JOIN account a ON d.account_id = a.account_id JOIN trans t ON a.account_id = t.account_id WHERE c.gender = 'M' AND c.birth_date BETWEEN '1974-01-01' AND '1976-12-31' AND t.amount > 4000 AND t.k_symbol = 'SIPO'
SELECT COUNT(*) FROM account a JOIN district d ON a.district_id = d.district_id WHERE d.A2 = 'Beroun' AND a.`date` > '1996-12-31'
SELECT count(T1.client_id) FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN account AS T3 ON T2.account_id = T3.account_id INNER JOIN card AS T4 ON T2.disp_id = T4.disp_id WHERE T1.gender = 'F' AND T4.type = 'junior'
SELECT CAST(SUM(CASE WHEN T1.gender = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM client AS T1 JOIN account AS T2 ON T1.client_id = T2.account_id JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T3.A3 = 'Prague'
SELECT CAST(SUM(CASE WHEN c.gender = 'M' THEN 1 ELSE 0 END) AS REAL) / COUNT(c.client_id) * 100 AS percentage_of_male_clients_requesting_weekly_statements FROM client c JOIN account a ON c.district_id = a.district_id WHERE a.frequency = 'POPLATEK TYDNE'
SELECT COUNT(d.client_id) FROM disp d JOIN account a ON d.account_id = a.account_id WHERE a.frequency = 'POPLATEK TYDNE' AND d.type = 'OWNER'
SELECT a.account_id FROM account a JOIN loan l ON a.account_id = l.account_id WHERE a.date < '1997-01-01' AND l.duration > 24 AND l.amount = ( SELECT MIN(l.amount) AS min_amount FROM loan l JOIN (SELECT a.account_id FROM account a JOIN (SELECT account_id FROM loan WHERE duration > 24) AS l ON a.account_id = l.account_id WHERE a.date < '1997-01-01') AS filtered_accounts ON l.account_id = filtered_accounts.account_id )
SELECT a.account_id FROM client c JOIN district d ON c.district_id = d.district_id JOIN disp a ON c.client_id = a.client_id WHERE c.gender = 'F' ORDER BY c.birth_date ASC, d.A11 ASC LIMIT 1
SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A3 = 'east Bohemia' AND STRFTIME('%Y', T1.birth_date) = '1920'
SELECT COUNT(*) FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.duration = 24 AND T2.frequency = 'POPLATEK TYDNE'
SELECT AVG(l.amount) FROM loan l JOIN account a ON l.account_id = a.account_id WHERE l.status = 'C' AND a.frequency = 'POPLATEK PO OBRATU'
SELECT DISTINCT T1.client_id, T2.district_id FROM disp AS T1 INNER JOIN client AS T2 ON T1.client_id = T2.client_id WHERE T1.type = 'OWNER'
SELECT c.client_id, STRFTIME('%Y', DATE('now')) - STRFTIME('%Y', c.birth_date) AS age FROM card cd JOIN disp d ON cd.disp_id = d.disp_id JOIN client c ON d.client_id = c.client_id WHERE cd.type = 'gold' AND d.type = 'OWNER'
SELECT bond_type FROM bond GROUP BY bond_type ORDER BY COUNT(bond_type) DESC LIMIT 1
SELECT COUNT(DISTINCT t1.molecule_id) FROM atom AS t1 INNER JOIN molecule AS t2 ON t1.molecule_id = t2.molecule_id WHERE t2.label = '-' AND t1.element = 'cl'
SELECT AVG(CASE WHEN a.element = 'o' THEN 1 ELSE 0 END) AS average_oxygen_atoms FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE b.bond_type = '-'
SELECT CAST(SUM(CASE WHEN b.bond_type = '-' THEN 1 ELSE 0 END) AS REAL) / COUNT(a.atom_id) AS average_single_bonded_atoms FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE m.label = '+'
SELECT COUNT(DISTINCT T2.molecule_id) FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.element = 'na' AND T1.label = '-'
SELECT DISTINCT T2.molecule_id FROM molecule AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.bond_type = '#' AND T1.label = '+'
SELECT CAST(COUNT(CASE WHEN T1.element = 'c' THEN 1 END) AS REAL) * 100 / COUNT(T1.element) FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_type = '='
SELECT COUNT(*) FROM bond WHERE bond_type = '#'
SELECT COUNT(*) FROM atom WHERE element != 'br'
SELECT COUNT(*) FROM molecule WHERE molecule_id BETWEEN 'TR000' AND 'TR099' AND label = '+'
SELECT DISTINCT molecule_id FROM atom WHERE element = 'c'
SELECT DISTINCT T2.element FROM connected AS T1 JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T1.bond_id = 'TR004_8_9'
SELECT DISTINCT T2.element, T3.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id INNER JOIN atom AS T3 ON T1.atom_id2 = T3.atom_id INNER JOIN bond AS T4 ON T1.bond_id = T4.bond_id WHERE T4.bond_type = '='
SELECT T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'h' GROUP BY T2.label ORDER BY COUNT(T2.label) DESC LIMIT 1
SELECT DISTINCT b.bond_type FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE a.element = 'cl'
SELECT T2.atom_id, T2.atom_id2 FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T1.bond_type = '-' GROUP BY T2.atom_id, T2.atom_id2
SELECT DISTINCT c.atom_id, c.atom_id2 FROM connected c JOIN bond b ON c.bond_id = b.bond_id JOIN molecule m ON b.molecule_id = m.molecule_id WHERE m.label = '-'
SELECT element FROM ( SELECT element, COUNT(*) AS element_count FROM ( SELECT * FROM molecule WHERE label = '-' ) m JOIN atom ON m.molecule_id = atom.molecule_id GROUP BY element ) AS element_counts ORDER BY element_count ASC LIMIT 1
SELECT bond_type FROM bond WHERE bond_id IN (SELECT bond_id FROM connected WHERE (atom_id = 'TR004_8' AND atom_id2 = 'TR004_20') OR (atom_id = 'TR004_20' AND atom_id2 = 'TR004_8'))
SELECT label FROM molecule WHERE molecule_id NOT IN (SELECT molecule_id FROM atom WHERE element = 'sn')
SELECT COUNT(DISTINCT CASE WHEN a.element = 'i' THEN a.atom_id END) + COUNT(DISTINCT CASE WHEN a.element = 's' THEN a.atom_id END) AS total_iodine_sulfur_atoms FROM atom a JOIN connected c ON a.atom_id = c.atom_id OR a.atom_id = c.atom_id2 JOIN bond b ON c.bond_id = b.bond_id WHERE b.bond_type = '-'
SELECT DISTINCT T1.atom_id, T1.atom_id2 FROM connected AS T1 INNER JOIN bond AS T2 ON T1.bond_id = T2.bond_id WHERE T2.bond_type = '#'
SELECT atom_id2 FROM connected WHERE bond_id IN ( SELECT bond_id FROM connected WHERE atom_id IN ( SELECT atom_id FROM atom WHERE molecule_id = 'TR181' ) ) UNION SELECT atom_id FROM connected WHERE bond_id IN ( SELECT bond_id FROM connected WHERE atom_id2 IN ( SELECT atom_id FROM atom WHERE molecule_id = 'TR181' ) )
SELECT CAST(SUM(CASE WHEN a.element != 'f' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(m.molecule_id) AS percentage FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+'
SELECT (SUM(CASE WHEN b.bond_type = '#' THEN 1 ELSE 0 END) * 100.0 / COUNT(b.bond_id)) AS percentage FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE m.label = '+'
SELECT element FROM atom WHERE molecule_id = 'TR000' ORDER BY element ASC LIMIT 3
SELECT atom_id, atom_id2 FROM connected WHERE bond_id = 'TR001_2_6'
SELECT SUM(CASE WHEN label = '+' THEN 1 ELSE 0 END) - SUM(CASE WHEN label = '-' THEN 1 ELSE 0 END) AS difference FROM molecule
SELECT atom_id, atom_id2 FROM connected WHERE bond_id = 'TR000_2_5'
SELECT bond_id FROM connected WHERE atom_id2 = 'TR000_2'
SELECT m.label FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE b.bond_type = ' = ' ORDER BY m.molecule_id ASC LIMIT 5
SELECT CAST(SUM(CASE WHEN bond_type = '=' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(bond_id) AS percentage FROM bond WHERE molecule_id = 'TR008'
SELECT ROUND(CAST(SUM(CASE WHEN label = '+' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(molecule_id), 3) AS percent FROM molecule
SELECT CAST(COUNT(CASE WHEN element = 'h' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) AS percent FROM atom WHERE molecule_id = 'TR206'
SELECT DISTINCT bond_type FROM bond WHERE molecule_id = 'TR000'
SELECT DISTINCT T1.element, T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR060'
SELECT T.bond_type, T2.label FROM ( SELECT bond_type, COUNT(*) AS bond_count FROM bond WHERE molecule_id = 'TR010' GROUP BY bond_type ORDER BY bond_count DESC LIMIT 1 ) AS T JOIN molecule AS T2 ON T2.molecule_id = 'TR010'
SELECT DISTINCT m1.molecule_id FROM molecule AS m1 JOIN bond AS b1 ON m1.molecule_id = b1.molecule_id WHERE m1.label = '-' AND b1.bond_type = '-' ORDER BY m1.molecule_id LIMIT 3
SELECT bond_id FROM bond WHERE molecule_id = 'TR006' ORDER BY bond_id LIMIT 2
SELECT COUNT(DISTINCT c.bond_id) FROM connected c JOIN bond b ON c.bond_id = b.bond_id WHERE b.molecule_id = 'TR009' AND (c.atom_id = 'TR009_12' OR c.atom_id2 = 'TR009_12')
SELECT COUNT(DISTINCT m.molecule_id) FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+' AND a.element = 'br'
SELECT T2.bond_type, T1.atom_id, T1.atom_id2 FROM connected AS T1 INNER JOIN bond AS T2 ON T1.bond_id = T2.bond_id WHERE T1.bond_id = 'TR001_6_9'
SELECT T2.molecule_id, T2.label FROM atom AS T1 JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.atom_id = 'TR001_10'
SELECT COUNT(DISTINCT molecule_id) FROM bond WHERE bond_type = '#'
SELECT COUNT(bond_id) FROM connected WHERE atom_id LIKE 'TR%_19'
SELECT element FROM atom WHERE molecule_id = 'TR004'
SELECT COUNT(*) FROM molecule WHERE label = '-'
SELECT DISTINCT a.molecule_id FROM atom a JOIN (SELECT molecule_id FROM molecule WHERE label = '+') m ON a.molecule_id = m.molecule_id WHERE SUBSTR(a.atom_id, 7, 2) BETWEEN '21' AND '25' ORDER BY a.molecule_id
SELECT DISTINCT c.bond_id FROM connected c JOIN atom a1 ON c.atom_id = a1.atom_id AND a1.element = 'p' JOIN atom a2 ON c.atom_id2 = a2.atom_id AND a2.element = 'n' WHERE c.bond_id IN (SELECT bond_id FROM bond)
SELECT m.label FROM molecule m JOIN ( SELECT molecule_id, COUNT(*) AS double_bond_count FROM bond WHERE bond_type = '=' GROUP BY molecule_id ORDER BY double_bond_count DESC LIMIT 1 ) AS most_double_bonds ON m.molecule_id = most_double_bonds.molecule_id
SELECT AVG(num_bonds) AS average_bonds FROM (SELECT atom_id, COUNT(bond_id) AS num_bonds FROM (SELECT a.atom_id, c.bond_id FROM atom a JOIN connected c ON a.atom_id = c.atom_id WHERE a.element = 'i') AS iodine_atoms GROUP BY atom_id) AS iodine_bonds_count
SELECT T2.bond_type, T2.bond_id FROM connected AS T1 INNER JOIN bond AS T2 ON T1.bond_id = T2.bond_id WHERE SUBSTR(T1.atom_id, 7, 2) + 0 = 45
SELECT element FROM atom WHERE atom_id NOT IN (SELECT atom_id FROM connected)
SELECT DISTINCT T1.atom_id, T1.atom_id2 FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id INNER JOIN atom AS T3 ON T1.atom_id2 = T3.atom_id INNER JOIN bond AS T4 ON T1.bond_id = T4.bond_id WHERE T2.molecule_id = 'TR041' AND T3.molecule_id = 'TR041' AND T4.bond_type = '#'
SELECT a1.element, a2.element FROM atom a1 JOIN connected c ON a1.atom_id = c.atom_id JOIN atom a2 ON c.atom_id2 = a2.atom_id WHERE c.bond_id = 'TR144_8_19'
SELECT m.molecule_id FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id JOIN connected c ON b.bond_id = c.bond_id WHERE m.label = '+' AND b.bond_type = '=' GROUP BY m.molecule_id ORDER BY COUNT(b.bond_id) DESC LIMIT 1
SELECT element FROM ( SELECT a.element, COUNT(*) AS element_count FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+' GROUP BY a.element ) AS element_counts ORDER BY element_counts.element_count ASC LIMIT 1
SELECT DISTINCT T2.atom_id2 FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T1.element = 'pb'
SELECT DISTINCT T1.element FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_type = '#'
SELECT CAST(COUNT(CASE WHEN c.bond_id IN ( SELECT bond_id FROM connected JOIN atom a1 ON connected.atom_id = a1.atom_id JOIN atom a2 ON connected.atom_id2 = a2.atom_id WHERE (a1.element, a2.element) = ( SELECT a1.element, a2.element FROM connected JOIN atom a1 ON connected.atom_id = a1.atom_id JOIN atom a2 ON connected.atom_id2 = a2.atom_id GROUP BY a1.element, a2.element ORDER BY COUNT(*) DESC LIMIT 1 ) ) THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(c.bond_id) AS percentage FROM connected c
SELECT CAST(SUM(CASE WHEN m.label = '+' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(b.bond_id) AS proportion FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_type = '-'
SELECT COUNT(*) FROM atom WHERE element IN ('c', 'h')
SELECT atom_id2 FROM connected WHERE atom_id IN (SELECT atom_id FROM atom WHERE element = 's')
SELECT DISTINCT b.bond_type FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE a.element = 'sn'
SELECT COUNT(DISTINCT T1.element) FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_type = '-'
SELECT COUNT(DISTINCT a.atom_id) FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE b.bond_type = '#' AND a.element IN ('p', 'br')
SELECT b.bond_id FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE m.label = '+'
SELECT DISTINCT b.molecule_id FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_type = '-' AND m.label = '-'
SELECT (CAST(SUM(CASE WHEN a1.element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*)) AS chlorine_percentage FROM atom a1 JOIN connected c ON a1.atom_id = c.atom_id JOIN atom a2 ON a2.atom_id = c.atom_id2 JOIN bond b ON c.bond_id = b.bond_id WHERE b.bond_type = '-'
SELECT label FROM molecule WHERE molecule_id IN ('TR000', 'TR001', 'TR002')
SELECT molecule_id FROM molecule WHERE label = '-'
SELECT COUNT(*) FROM molecule WHERE label = '+' AND molecule_id BETWEEN 'TR000' AND 'TR030'
SELECT bond_type FROM bond WHERE molecule_id BETWEEN 'TR000' AND 'TR050'
SELECT a1.element, a2.element FROM connected c JOIN atom a1 ON c.atom_id = a1.atom_id JOIN atom a2 ON c.atom_id2 = a2.atom_id WHERE c.bond_id = 'TR001_10_11'
SELECT COUNT(DISTINCT T2.bond_id) FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T1.element = 'i'
SELECT CASE WHEN SUM(CASE WHEN T1.label = '+' THEN 1 ELSE 0 END) > SUM(CASE WHEN T1.label = '-' THEN 1 ELSE 0 END) THEN '+' ELSE '-' END AS majority_label FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.element = 'ca'
SELECT CASE WHEN a1.element = 'cl' AND a2.element = 'c' OR a1.element = 'c' AND a2.element = 'cl' THEN 'Yes' ELSE 'No' END AS has_chlorine_and_carbon FROM connected c JOIN atom a1 ON c.atom_id = a1.atom_id JOIN atom a2 ON c.atom_id2 = a2.atom_id WHERE c.bond_id = 'TR001_1_8'
SELECT molecule_id FROM ( SELECT molecule_id FROM atom WHERE element = 'c' INTERSECT SELECT molecule_id FROM bond WHERE bond_type = '#' INTERSECT SELECT molecule_id FROM molecule WHERE label = '-' ) LIMIT 2
SELECT CAST(SUM(CASE WHEN T2.element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+'
SELECT element FROM atom WHERE molecule_id = 'TR001'
SELECT molecule_id FROM bond WHERE bond_type = '='
SELECT DISTINCT T1.atom_id, T1.atom_id2 FROM connected AS T1 INNER JOIN bond AS T2 ON T1.bond_id = T2.bond_id WHERE T2.bond_type = '#'
SELECT DISTINCT T2.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T1.bond_id = 'TR000_1_2' UNION SELECT DISTINCT T2.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id2 = T2.atom_id WHERE T1.bond_id = 'TR000_1_2'
SELECT COUNT(DISTINCT m.molecule_id) FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE m.label = '-' AND b.bond_type = '-'
SELECT m.label FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_id = 'TR001_10_11'
SELECT T.bond_id, T2.label FROM bond AS T JOIN molecule AS T2 ON T.molecule_id = T2.molecule_id WHERE T.bond_type = '#'
SELECT element FROM atom JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '+' AND substr(atom.atom_id, 7, 1) = '4'
SELECT CAST(SUM(CASE WHEN atom.element = 'h' THEN 1 ELSE 0 END) AS REAL) / COUNT(atom.element) AS ratio, molecule.label FROM atom JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE atom.molecule_id = 'TR006'
SELECT DISTINCT m.label FROM atom a JOIN molecule m ON a.molecule_id = m.molecule_id WHERE a.element = 'ca'
SELECT DISTINCT T1.bond_type FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id INNER JOIN atom AS T3 ON T2.atom_id = T3.atom_id WHERE T3.element = 'c'
SELECT element FROM atom WHERE atom_id = (SELECT atom_id FROM connected WHERE bond_id = 'TR001_10_11') UNION SELECT element FROM atom WHERE atom_id = (SELECT atom_id2 FROM connected WHERE bond_id = 'TR001_10_11')
SELECT CAST(COUNT(DISTINCT molecule_id) AS REAL) * 100 / (SELECT COUNT(*) FROM molecule) FROM bond WHERE bond_type = '#'
SELECT CAST(SUM(CASE WHEN bond_type = '=' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(bond_id) AS percent FROM bond WHERE molecule_id = 'TR047'
SELECT m.label FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE a.atom_id = 'TR001_1'
SELECT label FROM molecule WHERE molecule_id = 'TR151'
SELECT element FROM atom WHERE molecule_id = 'TR151' AND element IN ('cl', 'br', 'f', 'i', 'pb')
SELECT COUNT(*) FROM molecule WHERE label = '+'
SELECT atom_id FROM atom WHERE element = 'c' AND CAST(SUBSTR(molecule_id, 3, 3) AS INTEGER) BETWEEN 10 AND 50
SELECT COUNT(atom_id) FROM molecule JOIN atom ON molecule.molecule_id = atom.molecule_id WHERE molecule.label = '+'
SELECT b.bond_id FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE m.label = '+' AND b.bond_type = '='
SELECT COUNT(a.atom_id) FROM atom a JOIN molecule m ON a.molecule_id = m.molecule_id WHERE m.label = '+' AND a.element = 'h'
SELECT molecule_id FROM bond WHERE bond_id = 'TR000_1_2'
SELECT atom_id FROM atom JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE element = 'c' AND label = '-'
SELECT CAST(COUNT(CASE WHEN T2.element = 'h' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.label = '+'
SELECT label FROM molecule WHERE molecule_id = 'TR124'
SELECT atom_id FROM atom WHERE molecule_id = 'TR186'
SELECT bond_type FROM bond WHERE bond_id = 'TR007_4_19'
SELECT DISTINCT a.element FROM connected c JOIN atom a ON c.atom_id = a.atom_id WHERE c.bond_id = 'TR001_2_4'
SELECT (SELECT COUNT(*) FROM bond WHERE molecule_id = 'TR006' AND bond_type = '=') AS double_bonds_count, (SELECT label FROM molecule WHERE molecule_id = 'TR006') AS molecule_label
SELECT m.molecule_id, a.element  FROM molecule m  JOIN atom a  ON m.molecule_id = a.molecule_id  WHERE m.label = '+'  GROUP BY m.molecule_id, a.element
SELECT c.bond_id, c.atom_id, c.atom_id2 FROM bond b JOIN connected c ON b.bond_id = c.bond_id WHERE b.bond_type = '-'
SELECT DISTINCT element FROM atom WHERE molecule_id IN ( SELECT molecule_id FROM bond WHERE bond_type = '#' )
SELECT DISTINCT T2.element, T3.element FROM connected AS T1 JOIN atom AS T2 ON T1.atom_id = T2.atom_id JOIN atom AS T3 ON T1.atom_id2 = T3.atom_id WHERE T1.bond_id = 'TR000_2_3'
SELECT COUNT(DISTINCT c.bond_id) FROM atom a JOIN connected c ON a.atom_id = c.atom_id WHERE a.element = 'cl' OR a.element = 'cl'
SELECT a.atom_id, COUNT(DISTINCT b.bond_type) AS bond_type_count FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE a.molecule_id = 'TR346' GROUP BY a.atom_id
SELECT COUNT(DISTINCT b.molecule_id) AS double_bond_carcinogens FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_type = '=' AND m.label = '+'
SELECT COUNT(DISTINCT molecule_id) FROM molecule WHERE molecule_id NOT IN ( SELECT DISTINCT molecule_id FROM bond WHERE bond_type = '=' ) AND molecule_id NOT IN ( SELECT DISTINCT molecule_id FROM atom WHERE element = 's' )
SELECT m.label FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE b.bond_id = 'TR001_2_4'
SELECT COUNT(atom_id) FROM atom WHERE molecule_id = 'TR001'
SELECT COUNT(bond_id) FROM bond WHERE bond_type = '-'
SELECT T1.molecule_id FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.element = 'cl' AND T1.label = '+'
SELECT DISTINCT T1.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'c' AND T2.label = '-'
SELECT CAST(SUM(CASE WHEN a.element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+'
SELECT molecule_id FROM bond WHERE bond_id = 'TR001_1_7'
SELECT COUNT(DISTINCT a1.element) AS element_count FROM connected c JOIN atom a1 ON c.atom_id = a1.atom_id JOIN atom a2 ON c.atom_id2 = a2.atom_id WHERE c.bond_id = 'TR001_3_4'
SELECT b.bond_type FROM connected c JOIN bond b ON c.bond_id = b.bond_id WHERE c.atom_id = 'TR000_1' AND c.atom_id2 = 'TR000_2'
SELECT T1.molecule_id FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = "TR000_2" AND T2.atom_id2 = "TR000_4"
SELECT element FROM atom WHERE atom_id = 'TR000_1'
SELECT label FROM molecule WHERE molecule_id = 'TR000'
SELECT CAST(SUM(CASE WHEN bond_type = '-' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(bond_id) AS percentage FROM bond
SELECT COUNT(DISTINCT m.molecule_id) FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id JOIN connected c ON a.atom_id = c.atom_id WHERE m.label = '+' AND a.element = 'n'
SELECT DISTINCT T1.molecule_id FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id2 INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T1.element = 's' AND T3.bond_type = '='
SELECT m.molecule_id FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '-' GROUP BY m.molecule_id HAVING COUNT(a.atom_id) > 5
SELECT DISTINCT T1.element FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_type = '=' AND T1.molecule_id = 'TR024'
SELECT m.molecule_id FROM molecule m JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+' GROUP BY m.molecule_id ORDER BY COUNT(a.atom_id) DESC LIMIT 1
SELECT CASE WHEN COUNT(DISTINCT a.molecule_id) = 0 THEN 0 ELSE (COUNT(DISTINCT CASE WHEN m.label = '+' THEN m.molecule_id ELSE NULL END) * 100.0 / COUNT(DISTINCT a.molecule_id)) END AS percentage FROM connected c JOIN atom a ON c.atom_id = a.atom_id JOIN bond b ON c.bond_id = b.bond_id JOIN molecule m ON a.molecule_id = m.molecule_id WHERE a.element = 'h' AND b.bond_type = '#'
SELECT COUNT(molecule_id) FROM molecule WHERE label = '+'
SELECT COUNT(DISTINCT molecule_id) FROM ( SELECT molecule_id FROM bond WHERE molecule_id BETWEEN 'TR004' AND 'TR010' AND bond_type = '-' ) AS has_single_bond
SELECT COUNT(atom_id) FROM atom WHERE molecule_id = 'TR008' AND element = 'c'
SELECT element FROM atom WHERE atom_id = 'TR004_7' AND molecule_id IN (SELECT molecule_id FROM molecule WHERE label = '-')
SELECT COUNT(DISTINCT T1.molecule_id) FROM atom AS T1 JOIN connected AS T2 ON T1.atom_id = T2.atom_id JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_type = '=' AND T1.element = 'o'
SELECT COUNT(DISTINCT m.molecule_id) FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE b.bond_type = '#' AND m.label = '-'
SELECT DISTINCT a.element, b.bond_type FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE a.molecule_id = 'TR002'
SELECT T1.atom_id FROM (SELECT atom_id, atom_id2 FROM connected WHERE bond_id IN (SELECT bond_id FROM bond WHERE molecule_id = 'TR012' AND bond_type = '=')) AS T1 JOIN atom AS T2 ON T1.atom_id = T2.atom_id OR T1.atom_id2 = T2.atom_id WHERE T2.element = 'c'
SELECT atom_id FROM atom WHERE molecule_id IN (SELECT molecule_id FROM molecule WHERE label = '+') AND element = 'o'
SELECT name FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT name FROM cards WHERE borderColor = 'borderless' AND (cardKingdomFoilId IS NULL OR cardKingdomId IS NULL)
SELECT name FROM cards WHERE faceConvertedManaCost = (SELECT MAX(faceConvertedManaCost) FROM cards)
SELECT name FROM cards WHERE frameVersion = '2015' AND edhrecRank < 100
SELECT T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'mythic' AND T2.format = 'gladiator' AND T2.status = 'Banned'
SELECT l.status FROM cards c JOIN legalities l ON c.uuid = l.uuid WHERE c.types = 'Artifact' AND c.side IS NULL AND l.format = 'vintage'
SELECT c.id, c.artist FROM cards c JOIN legalities l ON c.uuid = l.uuid WHERE (c.power = '*' OR c.power IS NULL) AND l.format = 'commander' AND l.status = 'Legal'
SELECT c.id, r.text, c.hasContentWarning FROM cards c JOIN rulings r ON c.uuid = r.uuid WHERE c.artist = 'Stephen Daniele'
SELECT T2.text FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Sublime Epiphany' AND T1.number = '74s'
SELECT c.name, c.artist, c.isPromo FROM cards c JOIN rulings r ON c.uuid = r.uuid GROUP BY c.uuid ORDER BY COUNT(r.id) DESC LIMIT 1
SELECT fd.`language` FROM cards c JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.name = 'Annul' AND c.number = '29'
SELECT DISTINCT name FROM foreign_data WHERE `language` = 'Japanese'
SELECT CAST(COUNT(CASE WHEN language = 'Chinese Simplified' THEN id END) AS REAL) * 100 / COUNT(*) AS percentage FROM foreign_data
SELECT st.translation, s.totalSetSize FROM set_translations st JOIN sets s ON st.setCode = s.code WHERE st.language = 'Italian'
SELECT COUNT(DISTINCT types) FROM cards WHERE artist = 'Aaron Boyd'
SELECT keywords FROM cards WHERE name = 'Angel of Mercy'
SELECT COUNT(*) FROM cards WHERE power = '*'
SELECT promoTypes FROM cards WHERE name = 'Duress'
SELECT borderColor FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT originalType FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT DISTINCT T1.language FROM set_translations AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code INNER JOIN cards AS T3 ON T2.code = T3.setCode WHERE T3.name = 'Angel of Mercy'
SELECT COUNT(*) FROM legalities l JOIN cards c ON l.uuid = c.uuid WHERE l.status = 'Restricted' AND c.isTextless = 0
SELECT T2.text FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Condemn'
SELECT COUNT(c.id) FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE l.status = 'Restricted' AND c.isStarter = 1
SELECT legalities.status FROM cards JOIN legalities ON cards.uuid = legalities.uuid WHERE cards.name = 'Cloudchaser Eagle'
SELECT type FROM cards WHERE name = 'Benalish Knight'
SELECT DISTINCT T2.format FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Benalish Knight'
SELECT DISTINCT T1.artist FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'Phyrexian'
SELECT CAST(SUM(IIF(borderColor = 'borderless', 1, 0)) AS REAL) * 100 / COUNT(*) FROM cards
SELECT COUNT(DISTINCT cards.id) FROM cards WHERE isReprint = 1 AND uuid IN (SELECT uuid FROM foreign_data WHERE `language` = 'German')
SELECT COUNT(*) FROM cards c JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.borderColor = 'borderless' AND fd.language = 'Russian'
SELECT CAST(SUM(CASE WHEN T2.`language` = 'French' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.isStorySpotlight = 1
SELECT COUNT(id) FROM cards WHERE toughness = '99'
SELECT name FROM cards WHERE artist = 'Aaron Boyd'
SELECT COUNT(*) FROM cards WHERE borderColor = 'black' AND availability = 'mtgo'
SELECT id FROM cards WHERE convertedManaCost = 0
SELECT layout FROM cards WHERE keywords LIKE '%Flying%'
SELECT COUNT(id) FROM cards WHERE originalType = 'Summon - Angel' AND subtypes != 'Angel'
SELECT id FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT id FROM cards WHERE duelDeck = 'a'
SELECT edhrecRank FROM cards WHERE frameVersion = '2015'
SELECT DISTINCT T1.artist FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T2.language = 'Chinese Simplified'
SELECT c.name FROM cards c INNER JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.availability = 'paper' AND fd.language = 'Japanese'
SELECT COUNT(T1.id) FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.borderColor = 'white' AND T2.status = 'Banned'
SELECT T1.uuid, T2.language FROM legalities AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.format = 'legacy'
SELECT T1.text FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.name = 'Beacon of Immortality'
SELECT COUNT(c.id) AS number_of_cards, l.status FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE c.frameVersion = 'future' GROUP BY l.status
SELECT c.colors FROM cards c JOIN sets s ON c.setCode = s.code WHERE s.code = 'OGW'
SELECT st.translation, st.language FROM cards c JOIN set_translations st ON c.setCode = st.setCode WHERE c.setCode = '10E' AND c.convertedManaCost = 5
SELECT T1.name, T2.date FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.originalType = 'Creature - Elf'
SELECT T1.colors, T2.format FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.id BETWEEN 1 AND 20
SELECT DISTINCT T1.name FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.originalType = 'Artifact' AND T1.colors LIKE '%B%' AND T2.language IS NOT NULL
SELECT c.name FROM cards c JOIN rulings r ON c.uuid = r.uuid WHERE c.rarity = 'uncommon' ORDER BY r.date ASC LIMIT 3
SELECT COUNT(id) FROM cards WHERE artist = 'John Avon' AND cardKingdomFoilId IS NULL
SELECT COUNT(*) FROM cards WHERE borderColor = 'white' AND cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT COUNT(*) FROM cards WHERE artist = 'UDON' AND availability = 'mtgo' AND hand = '-1'
SELECT COUNT(*) FROM cards WHERE frameVersion = '1993' AND availability = 'paper' AND hasContentWarning = 1
SELECT manaCost FROM cards WHERE layout = 'normal' AND frameVersion = '2003' AND borderColor = 'black' AND availability = 'mtgo,paper'
SELECT SUM(CAST(SUBSTR(manaCost, INSTR(manaCost, '{') + 1, INSTR(manaCost, '}') - INSTR(manaCost, '{') - 1) AS REAL)) AS total_unconverted_mana FROM cards WHERE artist = 'Rob Alexander'
SELECT subtypes, supertypes FROM cards WHERE availability = 'arena'
SELECT setCode FROM set_translations WHERE language = 'Spanish'
SELECT CAST(SUM(CASE WHEN isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM cards WHERE frameEffects = 'legendary'
SELECT SUM(CASE WHEN isStorySpotlight = 1 AND isTextless = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS percentage, id FROM cards WHERE isStorySpotlight = 1 AND isTextless = 0
SELECT (COUNT(CASE WHEN T2.language = 'Spanish' THEN T1.uuid END) * 100.0 / COUNT(T1.uuid)) AS Percentage, T2.name FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid
SELECT T2.`language` FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.baseSetSize = 309
SELECT COUNT(DISTINCT sets.code) FROM sets JOIN set_translations ON sets.code = set_translations.setCode WHERE sets.block = 'Commander' AND set_translations.language = 'Portuguese (Brasil)'
SELECT DISTINCT T1.id FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.types = 'Creature' AND T2.status = 'Legal'
SELECT DISTINCT T1.type FROM foreign_data AS T1 JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.`language` = 'German' AND T2.subtypes IS NOT NULL AND T2.supertypes IS NOT NULL
SELECT COUNT(id) FROM cards WHERE (power IS NULL OR power = '*') AND text LIKE '%triggered ability%'
SELECT COUNT(*) FROM cards c JOIN legalities l ON c.uuid = l.uuid JOIN rulings r ON c.uuid = r.uuid WHERE l.format = 'premodern' AND r.text = 'This is a triggered mana ability.' AND c.side IS NULL
SELECT c.id FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE c.artist = 'Erica Yang' AND l.format = 'pauper' AND l.status = 'Legal' AND c.availability = 'paper'
SELECT artist FROM cards WHERE uuid = ( SELECT uuid FROM foreign_data WHERE text = 'Das perfekte Gegenmittel zu einer dichten Formation' )
SELECT T1.name FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.language = 'French' AND T2.type LIKE '%Creature%' AND T2.layout = 'normal' AND T2.borderColor = 'black' AND T2.artist = 'Matthew D. Wilson'
SELECT COUNT(T1.name) FROM cards AS T1 INNER JOIN rulings AS T2 ON T1.uuid = T2.uuid WHERE T1.rarity = 'rare' AND T2.date = '2007-02-01'
SELECT T2.language FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.block = 'Ravnica' AND T1.baseSetSize = 180
SELECT CAST(SUM(CASE WHEN T2.hasContentWarning = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM legalities AS T1 JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T1.format = 'commander' AND T1.status = 'Legal'
SELECT CAST(SUM(CASE WHEN T1.language = 'French' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM foreign_data AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.power IS NULL OR T2.power = '*'
SELECT CAST(SUM(CASE WHEN T1.type = 'expansion' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.code) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Japanese'
SELECT availability FROM cards WHERE artist = 'Daren Bader'
SELECT COUNT(*) FROM cards WHERE borderColor = 'borderless' AND edhrecRank > 12000
SELECT COUNT(*) FROM cards WHERE isOversized = 1 AND isReprint = 1 AND isPromo = 1
SELECT name FROM cards WHERE (power IS NULL OR power = '*') AND promoTypes LIKE '%arenaleague%' ORDER BY name LIMIT 3
SELECT `language` FROM foreign_data WHERE multiverseid = 149934
SELECT id FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL ORDER BY cardKingdomFoilId LIMIT 3
SELECT CAST(COUNT(CASE WHEN isTextless = 1 AND layout = 'normal' THEN 1 END) AS REAL) * 100 / COUNT(*) FROM cards
SELECT number FROM cards WHERE otherFaceIds IS NULL AND subtypes LIKE '%Angel%' AND subtypes LIKE '%Wizard%'
SELECT name FROM sets WHERE mtgoCode = '' OR mtgoCode IS NULL ORDER BY name ASC LIMIT 3
SELECT DISTINCT language FROM set_translations WHERE setCode = (SELECT code FROM sets WHERE mcmName = 'Archenemy' AND code = 'ARC')
SELECT s.name, st.translation FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE s.id = 5
SELECT type FROM sets WHERE id = 206
SELECT s.id, s.name FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.language = 'Italian' AND s.block = 'Shadowmoor' ORDER BY s.name LIMIT 2
SELECT s.id FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE s.isForeignOnly = 0 AND s.isFoilOnly = 1 AND st.language = 'Japanese'
SELECT s.name FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.language = 'Russian' ORDER BY s.baseSetSize DESC LIMIT 1
SELECT CAST(SUM(CASE WHEN T1.isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Chinese Simplified'
SELECT COUNT(*) FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.language = 'Japanese' AND (s.mtgoCode IS NULL OR s.mtgoCode = '')
SELECT id FROM cards WHERE borderColor = 'black'
SELECT id FROM cards WHERE frameEffects = 'extendedart'
SELECT name FROM cards WHERE borderColor = 'black' AND isFullArt = 1
SELECT `language` FROM set_translations WHERE id = 174
SELECT name FROM sets WHERE code = 'ALL'
SELECT language FROM foreign_data WHERE name = 'A Pedra Fellwar'
SELECT code FROM sets WHERE releaseDate = '2007-07-13'
SELECT baseSetSize, code FROM sets WHERE block IN ('Masques', 'Mirage')
SELECT code FROM sets WHERE type = 'expansion'
SELECT fd.name, fd.type FROM foreign_data fd JOIN cards c ON fd.uuid = c.uuid WHERE c.watermark = 'boros'
SELECT fd.language, fd.flavorText, c.type FROM cards c JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.watermark = 'colorpie'
SELECT CAST(COUNT(CASE WHEN T1.convertedManaCost = 10 THEN 1 END) AS REAL) * 100 / COUNT(*) FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = ( SELECT T2.name FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Abyssal Horror' ) AND T1.name = 'Abyssal Horror'
SELECT code FROM sets WHERE type = 'expansion' OR type = 'commander'
SELECT T2.name, T2.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.watermark = 'abzan'
SELECT T2.language, T2.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.watermark = 'azorius'
SELECT COUNT(*) FROM cards WHERE artist = 'Aaron Miller' AND cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
SELECT COUNT(*) FROM cards WHERE availability LIKE '%paper%' AND hand = '3'
SELECT name FROM cards WHERE isTextless = 0
SELECT manaCost FROM cards WHERE name = 'Ancestor''s Chosen'
SELECT COUNT(*) FROM cards WHERE borderColor = 'white' AND COALESCE(power, '*') = '*'
SELECT name FROM cards WHERE isPromo = 1 AND side IS NOT NULL
SELECT subtypes, supertypes FROM cards WHERE name = 'Molimo, Maro-Sorcerer'
SELECT purchaseUrls FROM cards WHERE promoTypes LIKE '%bundle%'
SELECT COUNT(DISTINCT artist) FROM cards WHERE borderColor = 'black' AND availability LIKE '%arena,mtgo%'
SELECT name FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1
SELECT artist FROM cards WHERE flavorName = 'Battra, Dark Destroyer'
SELECT name FROM cards WHERE frameVersion = '2003' ORDER BY convertedManaCost DESC LIMIT 3
SELECT st.translation FROM set_translations st JOIN sets s ON st.setCode = s.code JOIN cards c ON s.code = c.setCode WHERE c.name = 'Ancestor''s Chosen' AND st.language = 'Italian'
SELECT COUNT(*) AS total_translations FROM cards c JOIN set_translations st ON c.setCode = st.setCode WHERE c.name = 'Angel of Mercy'
SELECT name FROM cards WHERE setCode = (SELECT setCode FROM set_translations WHERE translation = 'Hauptset Zehnte Edition')
SELECT EXISTS(   SELECT 1   FROM cards c   JOIN foreign_data fd ON c.uuid = fd.uuid   WHERE c.name = 'Ancestor''s Chosen' AND fd.language = 'Korean' )
SELECT COUNT(*) FROM set_translations AS T1 INNER JOIN cards AS T2 ON T1.setCode = T2.setCode WHERE T1.translation = 'Hauptset Zehnte Edition' AND T2.artist = 'Adam Rex'
SELECT s.baseSetSize FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.translation = 'Hauptset Zehnte Edition'
SELECT translation FROM sets JOIN set_translations ON sets.code = set_translations.setCode WHERE sets.name = 'Eighth Edition' AND set_translations.language = 'Chinese Simplified'
SELECT CASE WHEN s.mtgoCode IS NOT NULL THEN 'Yes' ELSE 'No' END AS appeared_on_mtgo FROM sets s JOIN cards c ON s.code = c.setCode WHERE c.name = 'Angel of Mercy'
SELECT T2.releaseDate FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Ancestor''s Chosen'
SELECT type FROM sets WHERE code = (SELECT setCode FROM set_translations WHERE translation = 'Hauptset Zehnte Edition')
SELECT COUNT(DISTINCT T1.code) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Italian' AND T1.block = 'Ice Age' AND T2.translation IS NOT NULL
SELECT T1.isForeignOnly FROM sets AS T1 INNER JOIN cards AS T2 ON T1.code = T2.setCode WHERE T2.name = 'Adarkar Valkyrie'
SELECT SUM(IIF(T1.baseSetSize < 100, 1, 0)) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Italian'
SELECT COUNT(*) FROM sets s JOIN cards c ON s.code = c.setCode WHERE s.name = 'Coldsnap' AND c.borderColor = 'black'
SELECT c.name FROM cards c JOIN sets s ON c.setCode = s.code WHERE s.name = 'Coldsnap' ORDER BY c.convertedManaCost DESC LIMIT 1
SELECT DISTINCT T2.artist FROM sets AS T1 INNER JOIN cards AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Coldsnap' AND T2.artist IN ('Jeremy Jarvis', 'Aaron Miller', 'Chippy')
SELECT T2.name FROM sets AS T1 INNER JOIN cards AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Coldsnap' AND T2.number = 4
SELECT COUNT(*) FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap' AND T1.convertedManaCost > 5 AND (T1.power = '*' OR T1.power IS NULL)
SELECT T2.flavorText FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Ancestor''s Chosen' AND T2.language = 'Italian'
SELECT fd.language FROM cards c JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.name = 'Ancestor''s Chosen' AND fd.flavorText IS NOT NULL
SELECT T2.type FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.name LIKE 'Ancestor%s Chosen' AND T2.language = 'German'
SELECT fd.text FROM sets s JOIN cards c ON s.code = c.setCode JOIN rulings r ON c.uuid = r.uuid JOIN foreign_data fd ON r.uuid = fd.uuid WHERE s.name = 'Coldsnap' AND fd.language = 'Italian'
SELECT fd.name FROM foreign_data fd JOIN cards c ON fd.uuid = c.uuid JOIN sets s ON c.setCode = s.code WHERE s.name = 'Coldsnap' AND fd.language = 'Italian' ORDER BY c.convertedManaCost DESC LIMIT 1
SELECT r.date FROM cards c JOIN rulings r ON c.uuid = r.uuid WHERE c.name = 'Reminisce'
SELECT CAST(SUM(CASE WHEN T1.convertedManaCost = 7 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM cards AS T1 JOIN sets AS T2 ON T1.setCode = T2.code WHERE T2.name = 'Coldsnap'
SELECT CAST(SUM(CASE WHEN T2.cardKingdomFoilId IS NOT NULL AND T2.cardKingdomId IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM sets AS T1 INNER JOIN cards AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Coldsnap'
SELECT code FROM sets WHERE releaseDate = '2017-07-14'
SELECT keyruneCode FROM sets WHERE code = 'PKHC'
SELECT mcmId FROM sets WHERE code = 'SS2'
SELECT mcmName FROM sets WHERE releaseDate = '2017-06-09'
SELECT type FROM sets WHERE name = 'From the Vault: Lore'
SELECT parentCode FROM sets WHERE name = 'Commander 2014 Oversized'
SELECT r.text AS ruling_text, c.hasContentWarning FROM cards c JOIN rulings r ON c.uuid = r.uuid WHERE c.artist = 'Jim Pavelec'
SELECT DISTINCT T1.releaseDate FROM sets AS T1 INNER JOIN cards AS T2 ON T1.code = T2.setCode WHERE T2.name = 'Evacuation'
SELECT s.baseSetSize FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.translation = 'Rinascita di Alara'
SELECT s.type FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.translation = 'Huitième édition'
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setcode INNER JOIN cards AS T3 ON T1.code = T3.setCode WHERE T2.language = 'French' AND T3.name = 'Tendo Ice Bridge'
SELECT COUNT(T1.id) FROM set_translations AS T1 INNER JOIN sets AS T2 ON T1.setcode = T2.code WHERE T2.name = 'Tenth Edition'
SELECT st.translation FROM cards c JOIN sets s ON c.setCode = s.code JOIN set_translations st ON s.code = st.setCode AND st.language = 'Japanese' WHERE c.name = 'Fellwar Stone'
SELECT c.name FROM sets s JOIN cards c ON s.code = c.setCode WHERE s.name = 'Journey into Nyx Hero''s Path' ORDER BY c.convertedManaCost DESC LIMIT 1
SELECT T1.releaseDate FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.translation = 'Ola de frío'
SELECT DISTINCT T2.type FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.name = 'Samite Pilgrim'
SELECT COUNT(*) FROM sets s JOIN cards c ON s.code = c.setCode WHERE s.name = 'World Championship Decks 2004' AND c.convertedManaCost = 3
SELECT T2.translation FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T1.name = 'Mirrodin' AND T2.language = 'Chinese Simplified'
SELECT CAST(SUM(CASE WHEN s.isNonFoilOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage_non_foil FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.language = 'Japanese'
SELECT CAST(SUM(CASE WHEN s.isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage_online_only FROM set_translations st JOIN sets s ON st.setCode = s.code WHERE st.language = 'Portuguese (Brazil)'
SELECT availability FROM cards WHERE artist = 'Aleksi Briclot' AND isTextless = 1
SELECT id FROM sets WHERE baseSetSize = (SELECT MAX(baseSetSize) FROM sets)
SELECT artist FROM cards WHERE side IS NULL ORDER BY convertedManaCost DESC LIMIT 1
SELECT frameEffects FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL GROUP BY frameEffects ORDER BY COUNT(frameEffects) DESC LIMIT 1
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND hasFoil = 0 AND duelDeck = 'a'
SELECT id FROM sets WHERE type = 'commander' ORDER BY totalSetSize DESC LIMIT 1
SELECT c.name FROM cards c JOIN legalities l ON c.uuid = l.uuid WHERE l.format = 'duel' ORDER BY c.manaCost DESC LIMIT 10
SELECT c.originalReleaseDate, l.format FROM cards c JOIN legalities l ON c.uuid = l.uuid WHERE c.rarity = 'mythic' AND l.status = 'Legal' ORDER BY c.originalReleaseDate ASC LIMIT 1
SELECT COUNT(T1.id) FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.artist = 'Volkan Baǵa' AND T2.language = 'French'
SELECT COUNT(*) FROM cards JOIN legalities ON cards.uuid = legalities.uuid WHERE cards.rarity = 'rare' AND cards.types LIKE '%Enchantment%' AND cards.name = 'Abundance' AND legalities.status = 'Legal'
SELECT l.format, c.name FROM legalities l JOIN cards c ON l.uuid = c.uuid WHERE l.status = 'Banned' GROUP BY l.format ORDER BY COUNT(l.format) DESC LIMIT 1
SELECT code FROM sets WHERE name = 'Battlebond'
SELECT l.format FROM cards c JOIN legalities l ON c.uuid = l.uuid GROUP BY c.artist ORDER BY COUNT(c.id) ASC LIMIT 1
SELECT L.status FROM cards C JOIN legalities L ON C.uuid = L.uuid WHERE C.frameVersion = '1997' AND C.artist = 'D. Alexander Gregory' AND C.hasContentWarning = 1 AND L.format = 'legacy'
SELECT T1.name, T2.format FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.edhrecRank = 1 AND T2.status = 'Banned'
SELECT CAST(COUNT(*) AS REAL) / 4 AS annual_average_sets, (SELECT language FROM set_translations WHERE setCode IN (SELECT code FROM sets WHERE releaseDate BETWEEN '2012-01-01' AND '2015-12-31') GROUP BY language ORDER BY COUNT(*) DESC LIMIT 1) AS common_language FROM sets WHERE releaseDate BETWEEN '2012-01-01' AND '2015-12-31'
SELECT artist FROM cards WHERE borderColor = 'black' AND availability = 'arena'
SELECT uuid FROM legalities WHERE format = 'oldschool' AND status IN ('Restricted', 'Banned')
SELECT COUNT(*) FROM cards WHERE artist = 'Matthew D. Wilson' AND availability = 'paper'
SELECT T1.text FROM rulings AS T1 INNER JOIN cards AS T2 ON T1.uuid = T2.uuid WHERE T2.artist = 'Kev Walker' ORDER BY T1.date DESC
SELECT T1.name, T3.format FROM cards AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code INNER JOIN legalities AS T3 ON T1.uuid = T3.uuid WHERE T2.name = 'Hour of Devastation' AND T3.status = 'Legal'
SELECT name FROM sets WHERE code IN ( SELECT setCode FROM set_translations WHERE language = 'Korean' INTERSECT SELECT setCode FROM set_translations WHERE language != 'Japanese' )
SELECT frameVersion FROM cards UNION SELECT frameVersion FROM cards WHERE artist = 'Allen Williams' UNION SELECT c.frameVersion FROM cards c JOIN legalities l ON c.uuid = l.uuid WHERE l.status = 'Banned'
SELECT CASE WHEN (SELECT MAX(Reputation) FROM users WHERE DisplayName = 'Harlan') > (SELECT MAX(Reputation) FROM users WHERE DisplayName = 'Jarrod Dixon') THEN 'Harlan' ELSE 'Jarrod Dixon' END AS UserWithHigherReputation
SELECT DisplayName FROM users WHERE STRFTIME('%Y', CreationDate) = '2011'
SELECT COUNT(*) FROM users WHERE LastAccessDate > '2014-09-01'
SELECT DisplayName FROM users ORDER BY Views DESC LIMIT 1
SELECT COUNT(*) FROM users WHERE UpVotes > 100 AND DownVotes > 1
SELECT COUNT(*) FROM users WHERE Views > 10 AND STRFTIME('%Y', CreationDate) > '2013'
SELECT COUNT(*) FROM users JOIN posts ON users.Id = posts.OwnerUserId WHERE users.DisplayName = 'csgillespie'
SELECT T1.Title FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT u.DisplayName FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.Title = 'Eliciting priors from experts'
SELECT T2.Title FROM users AS T1 INNER JOIN posts AS T2 ON T1.Id = T2.OwnerUserId WHERE T1.DisplayName = 'csgillespie' ORDER BY T2.ViewCount DESC LIMIT 1
SELECT u.DisplayName FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.FavoriteCount = (SELECT MAX(FavoriteCount) FROM posts)
SELECT SUM(p.CommentCount) AS TotalNumber_of_Comments FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.DisplayName = 'csgillespie'
SELECT MAX(p.AnswerCount) AS MaxAnswerCount FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.DisplayName = 'csgillespie'
SELECT u.DisplayName FROM posts p JOIN users u ON p.LastEditorUserId = u.Id WHERE p.Title = 'Examples for teaching: Correlation does not mean causation'
SELECT COUNT(*) FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'csgillespie' AND p.ParentId IS NULL
SELECT DISTINCT t2.DisplayName FROM posts t1 JOIN users t2 ON t1.OwnerUserId = t2.Id WHERE t1.ClosedDate IS NOT NULL
SELECT COUNT(*) FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.Age > 65 AND p.Score >= 20
SELECT u.Location FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.Title = 'Eliciting priors from experts'
SELECT T2.Body FROM tags AS T1 INNER JOIN posts AS T2 ON T1.ExcerptPostId = T2.Id WHERE T1.TagName = 'bayesian'
SELECT p.Body  FROM posts p  JOIN tags t ON p.Id = t.ExcerptPostId  WHERE t.Count = (SELECT MAX(Count) FROM tags)
SELECT COUNT(b.Id) FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.DisplayName = 'csgillespie'
SELECT T1.Name FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'csgillespie'
SELECT COUNT(*) FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.DisplayName = 'csgillespie' AND STRFTIME('%Y', b.Date) = '2011'
SELECT u.DisplayName FROM badges b JOIN users u ON b.UserId = u.Id GROUP BY b.UserId ORDER BY COUNT(b.Id) DESC LIMIT 1
SELECT AVG(p.Score) FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'csgillespie'
SELECT AVG(badge_count) AS average_number_of_badges FROM ( SELECT UserId, COUNT(Id) AS badge_count FROM badges WHERE UserId IN ( SELECT Id FROM users WHERE Views > 200 ) GROUP BY UserId ) AS user_badge_counts
SELECT CAST(COUNT(CASE WHEN u.Age > 65 THEN 1 END) AS REAL) * 100 / COUNT(*) AS PercentageOfElderUserOwnedPosts FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.Score > 5
SELECT COUNT(*) FROM votes WHERE UserId = 58 AND CreationDate = '2010-07-19'
SELECT CreationDate FROM votes GROUP BY CreationDate ORDER BY COUNT(Id) DESC LIMIT 1
SELECT COUNT(*) FROM badges WHERE Name = 'Revival'
SELECT T2.Title FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id ORDER BY T1.Score DESC LIMIT 1
SELECT COUNT(c.Id) AS NumberOfComments FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.ViewCount = 1910
SELECT FavoriteCount FROM posts WHERE Id IN ( SELECT PostId FROM comments WHERE UserId = 3025 AND CreationDate = '2014-04-23 20:29:39.0' )
SELECT c.Text FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.ParentId = 107829 AND p.CommentCount = 1 LIMIT 1
SELECT CASE WHEN p.ClosedDate IS NULL THEN 'well-finished' ELSE 'not well-finished' END AS well_finished_status FROM comments c JOIN posts p ON c.PostId = p.Id WHERE c.UserId = 23853 AND c.CreationDate = '2013-07-12 09:08:18.0'
SELECT u.Reputation FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.Id = 65041
SELECT COUNT(*) FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.DisplayName = 'Tiago Pasqualini'
SELECT T2.DisplayName FROM votes AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Id = 6347
SELECT COUNT(v.Id) AS NumberOfVotes FROM posts p JOIN votes v ON p.Id = v.PostId WHERE p.Title LIKE '%data visualization%'
SELECT T1.Name FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'DatEpicCoderGuyWhoPrograms'
SELECT CAST(COUNT(DISTINCT p.Id) AS REAL) / COUNT(DISTINCT v.Id) AS PostToVoteRatio FROM posts p JOIN votes v ON p.Id = v.PostId WHERE p.OwnerUserId = 24 AND v.UserId = 24
SELECT ViewCount FROM posts WHERE Title = 'Integration of Weka and/or RapidMiner into Informatica PowerCenter/Developer'
SELECT Text FROM comments WHERE Score = 17
SELECT DisplayName FROM users WHERE WebsiteUrl = 'http://stackoverflow.com'
SELECT b.Name FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.DisplayName = 'SilentGhost'
SELECT u.DisplayName FROM comments c JOIN users u ON c.UserId = u.Id WHERE c.Text = 'thank you user93!'
SELECT c.Text FROM comments c JOIN users u ON c.UserId = u.Id WHERE u.DisplayName = 'A Lion'
SELECT u.DisplayName, u.Reputation FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE p.Title = 'Understanding what Dassault iSight is doing?'
SELECT c.Text FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.Title = 'How does gentle boosting differ from AdaBoost?'
SELECT DISTINCT u.DisplayName FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Name = 'Necromancer' LIMIT 10
SELECT u.DisplayName FROM posts p JOIN users u ON p.LastEditorUserId = u.Id WHERE p.Title = 'Open source tools for visualizing multi-dimensional data'
SELECT Title FROM posts WHERE LastEditorUserId = (SELECT Id FROM users WHERE DisplayName = 'Vebjorn Ljosa')
SELECT SUM(p.Score) AS TotalScore, u.WebsiteUrl FROM posts p JOIN users u ON p.LastEditorUserId = u.Id WHERE u.DisplayName = 'Yevgeny'
SELECT c.Text FROM comments c JOIN posts p ON c.PostId = p.Id WHERE p.Title = 'Why square the difference instead of taking the absolute value in standard deviation?'
SELECT SUM(COALESCE(v.BountyAmount, 0)) AS TotalBountyAmount FROM posts p JOIN votes v ON p.Id = v.PostId WHERE p.Title LIKE '%data%'
SELECT u.DisplayName  FROM votes v  JOIN posts p ON v.PostId = p.Id  JOIN users u ON v.UserId = u.Id  WHERE v.BountyAmount = 50 AND p.Title LIKE '%variance%'
SELECT AVG(ViewCount) AS average_view_count, Title, Text FROM posts JOIN comments ON posts.Id = comments.PostId WHERE Tags LIKE '%<humor>%' GROUP BY posts.Id, Title, Text
SELECT COUNT(*) FROM comments WHERE UserId = 13
SELECT Id FROM users WHERE Reputation = (SELECT MAX(Reputation) FROM users)
SELECT Id FROM users ORDER BY Views ASC LIMIT 1
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Supporter' AND STRFTIME('%Y', Date) = '2011'
SELECT COUNT(UserId) FROM ( SELECT UserId FROM badges GROUP BY UserId HAVING COUNT(Name) > 5 ) AS UsersWithMoreThan5Badges
SELECT COUNT(DISTINCT u.Id)  FROM users u  JOIN badges b1 ON u.Id = b1.UserId AND b1.Name = 'Supporter'  JOIN badges b2 ON u.Id = b2.UserId AND b2.Name = 'Teacher'  WHERE u.Location = 'New York'
SELECT T2.DisplayName, T2.Reputation FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.Id = 1
SELECT u.Id FROM users u JOIN postHistory ph ON u.Id = ph.UserId WHERE u.Views >= 1000 GROUP BY u.Id, ph.PostId HAVING COUNT(ph.Id) = 1
SELECT b.Name FROM badges b JOIN ( SELECT UserId FROM comments GROUP BY UserId ORDER BY COUNT(Id) DESC LIMIT 1 ) c ON b.UserId = c.UserId
SELECT COUNT(DISTINCT u.Id) FROM users u INNER JOIN badges b ON u.Id = b.UserId WHERE b.Name = 'Teacher' AND u.Location = 'India'
SELECT ((CAST(SUM(CASE WHEN STRFTIME('%Y', Date) = '2010' THEN 1 ELSE 0 END) AS REAL) / COUNT(Date)) - (CAST(SUM(CASE WHEN STRFTIME('%Y', Date) = '2011' THEN 1 ELSE 0 END) AS REAL) / COUNT(Date))) * 100 AS PercentageDifference FROM badges WHERE Name = 'Student'
SELECT PostHistoryTypeId FROM postHistory WHERE PostId = 3720 UNION SELECT COUNT(DISTINCT UserId) AS UniqueUserCount FROM comments WHERE PostId = 3720
SELECT ViewCount FROM posts WHERE Id IN (SELECT RelatedPostId FROM postLinks WHERE PostId = 61217)
SELECT T1.Score, T2.LinkTypeId FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId WHERE T1.Id = 395
SELECT Id, OwnerUserId FROM posts WHERE Score > 60
SELECT SUM(FavoriteCount) FROM posts WHERE OwnerUserId = 686 AND STRFTIME('%Y', CreaionDate) = '2011'
SELECT AVG(u.UpVotes) AS AverageUpVotes, AVG(u.Age) AS AverageAge FROM users u JOIN posts p ON u.Id = p.OwnerUserId GROUP BY u.Id HAVING COUNT(p.Id) > 10
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Announcer'
SELECT Name FROM badges WHERE Date = '2010-07-19 19:39:08.0'
SELECT COUNT(*) FROM comments WHERE Score > 60
SELECT Text FROM comments WHERE CreationDate = '2010-07-19 19:25:47.0'
SELECT COUNT(*) FROM posts WHERE Score = 10
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Reputation = ( SELECT MAX(Reputation) FROM users )
SELECT u.Reputation FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Date = '2010-07-19 19:39:08.0'
SELECT T1.Name FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Pierre'
SELECT b.Date FROM badges b INNER JOIN users u ON b.UserId = u.Id WHERE u.Location = 'Rochester, NY'
SELECT CAST(SUM(CASE WHEN Name = 'Teacher' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(UserId) AS TeacherPercentage FROM badges
SELECT CAST(COUNT(CASE WHEN u.Age BETWEEN 13 AND 18 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(b.UserId) AS PercentageTeenagers FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Name = 'Organizer'
SELECT Score FROM comments WHERE CreationDate = '2010-07-19 19:19:56.0'
SELECT Text FROM comments WHERE CreationDate = '2010-07-19 19:37:33.0'
SELECT u.Age FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.Location = 'Vienna, Austria'
SELECT COUNT(DISTINCT u.Id) FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Name = 'Supporter' AND u.Age BETWEEN 19 AND 65
SELECT u.views FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Date = '2010-07-19 19:39:08.0'
SELECT T1.Name FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Reputation = ( SELECT MIN(Reputation) FROM users )
SELECT T2.Name FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'Sharpie'
SELECT COUNT(*) FROM users AS T1  INNER JOIN badges AS T2 ON T1.Id = T2.UserId  WHERE T2.Name = 'Supporter' AND T1.Age > 65
SELECT DisplayName FROM users WHERE Id = 30
SELECT COUNT(*) FROM users WHERE Location = 'New York'
SELECT COUNT(*) FROM votes WHERE STRFTIME('%Y', CreationDate) = '2010'
SELECT COUNT(*) FROM users WHERE Age BETWEEN 19 AND 65
SELECT DisplayName FROM users WHERE Views = (SELECT MAX(Views) FROM users)
SELECT CAST(COUNT(CASE WHEN STRFTIME('%Y', CreationDate) = '2010' THEN Id ELSE NULL END) AS REAL) / COUNT(CASE WHEN STRFTIME('%Y', CreationDate) = '2011' THEN Id ELSE NULL END) AS ratio FROM votes
SELECT DISTINCT t.TagName FROM users u JOIN posts p ON u.Id = p.OwnerUserId OR u.Id = p.LastEditorUserId JOIN posthistory ph ON p.Id = ph.PostId JOIN tags t ON p.Tags LIKE '%' || t.TagName || '%' WHERE u.DisplayName = 'John Salvatier'
SELECT COUNT(*) FROM posts JOIN users ON posts.OwnerUserId = users.Id WHERE users.DisplayName = 'Daniel Vassallo'
SELECT COUNT(V.Id) FROM votes AS V JOIN users AS U ON V.UserId = U.Id WHERE U.DisplayName = 'Harlan'
SELECT p.Id FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'slashnick' ORDER BY p.AnswerCount DESC LIMIT 1
SELECT DisplayName FROM ( SELECT u.DisplayName, SUM(p.ViewCount) AS TotalViewCount FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.DisplayName IN ('Harvey Motulsky', 'Noah Snyder') GROUP BY u.DisplayName ORDER BY TotalViewCount DESC LIMIT 1 ) AS HigherPopularityUser
SELECT COUNT(*) FROM posts p JOIN users u ON p.OwnerUserId = u.Id JOIN votes v ON p.Id = v.PostId WHERE u.DisplayName = 'Matt Parker' GROUP BY p.Id HAVING COUNT(v.Id) > 4
SELECT COUNT(c.Id) FROM posts p JOIN comments c ON p.Id = c.PostId JOIN users u ON p.OwnerUserId = u.Id WHERE c.Score < 60 AND u.DisplayName = 'Neil McGuigan'
SELECT DISTINCT Tags FROM posts JOIN users ON posts.OwnerUserId = users.Id WHERE users.DisplayName = 'Mark Meckes' AND posts.CommentCount = 0
SELECT DISTINCT u.DisplayName FROM badges b JOIN users u ON b.UserId = u.Id WHERE b.Name = 'Organizer'
SELECT CAST(SUM(CASE WHEN p.Tags LIKE '%<r>%' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Community'
SELECT SUM(CASE WHEN u.DisplayName = 'Mornington' THEN p.ViewCount ELSE 0 END) - SUM(CASE WHEN u.DisplayName = 'Amos' THEN p.ViewCount ELSE 0 END) AS ViewCountDifference  FROM posts p  JOIN users u ON p.OwnerUserId = u.Id
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Commentator' AND STRFTIME('%Y', Date) = '2014'
SELECT COUNT(*) FROM posts WHERE date(CreaionDate) = '2010-07-21'
SELECT DisplayName, Age FROM users WHERE Views = (SELECT MAX(Views) FROM users)
SELECT LastEditDate, LastEditorUserId FROM posts WHERE Title = 'Detecting a given face in a database of facial images'
SELECT COUNT(*) FROM comments WHERE UserId = 13 AND Score < 60
SELECT T2.Title, T1.UserDisplayName FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T1.Score > 60
SELECT b.Name FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.Location = 'North Pole' AND STRFTIME('%Y', b.Date) = '2011'
SELECT u.DisplayName, u.WebsiteUrl  FROM posts p  JOIN users u ON p.OwnerUserId = u.Id  WHERE p.FavoriteCount > 150
SELECT COUNT(ph.PostId) AS post_history_counts, p.LastEditDate FROM posts p JOIN postHistory ph ON p.Id = ph.PostId WHERE p.Title = 'What is the best introductory Bayesian statistics textbook?'
SELECT T2.LastAccessDate, T2.Location FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name = 'outliers'
SELECT p2.Title FROM posts p1 JOIN postLinks pl ON p1.Id = pl.PostId JOIN posts p2 ON pl.RelatedPostId = p2.Id WHERE p1.Title = 'How to tell if something happened in a data set which monitors a value over time'
SELECT ph.PostId, b.Name FROM postHistory ph JOIN badges b ON ph.UserId = b.UserId WHERE ph.UserDisplayName = 'Samuel' AND strftime('%Y', ph.CreationDate) = '2013' AND strftime('%Y', b.Date) = '2013'
SELECT u.DisplayName  FROM posts p  JOIN users u ON p.OwnerUserId = u.Id  WHERE p.Id = (SELECT Id FROM posts ORDER BY ViewCount DESC LIMIT 1)
SELECT u.DisplayName, u.Location FROM tags t JOIN posts p ON t.ExcerptPostId = p.Id JOIN users u ON p.OwnerUserId = u.Id WHERE t.TagName = 'hypothesis-testing'
SELECT p.Title, pl.LinkTypeId FROM postLinks pl JOIN posts p ON pl.RelatedPostId = p.Id WHERE pl.PostId IN (SELECT Id FROM posts WHERE Title = 'What are principal component scores?')
SELECT u.DisplayName FROM posts p JOIN posts parent ON p.ParentId = parent.Id JOIN users u ON parent.OwnerUserId = u.Id WHERE p.ParentId IS NOT NULL ORDER BY p.Score DESC LIMIT 1
SELECT u.DisplayName, u.WebsiteUrl FROM users u JOIN votes v ON u.Id = v.UserId WHERE v.VoteTypeId = 8 AND v.BountyAmount = ( SELECT MAX(BountyAmount) FROM votes WHERE VoteTypeId = 8 )
SELECT Title FROM posts ORDER BY ViewCount DESC LIMIT 5
SELECT COUNT(*) FROM tags WHERE Count BETWEEN 5000 AND 7000
SELECT OwnerUserId FROM posts WHERE FavoriteCount = (SELECT MAX(FavoriteCount) FROM posts)
SELECT Age FROM users ORDER BY Reputation DESC LIMIT 1
SELECT COUNT(DISTINCT PostId) FROM votes WHERE STRFTIME('%Y', CreationDate) = '2011' AND BountyAmount = 50
SELECT Id FROM users WHERE Age = (SELECT MIN(Age) FROM users) LIMIT 1
SELECT SUM(Score) FROM posts WHERE LasActivityDate LIKE '2010-07-19%'
SELECT CAST(COUNT(DISTINCT pl.Id) AS REAL) / 12 AS AverageMonthlyLinks FROM postLinks pl JOIN posts p ON pl.PostId = p.Id WHERE p.AnswerCount <= 2 AND strftime('%Y', pl.CreationDate) = '2010'
SELECT p.Id FROM posts p JOIN votes v ON p.Id = v.PostId WHERE v.UserId = 1465 ORDER BY p.FavoriteCount DESC LIMIT 1
SELECT p.Title FROM posts p JOIN postLinks pl ON p.Id = pl.PostId ORDER BY pl.CreationDate ASC LIMIT 1
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T2.DisplayName ORDER BY COUNT(T1.Name) DESC LIMIT 1
SELECT MIN(v.CreationDate) AS FirstVoteDate FROM users u JOIN votes v ON u.Id = v.UserId WHERE u.DisplayName = 'chl'
SELECT MIN(p.CreaionDate) AS FirstPostDate FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.Age = (SELECT MIN(Age) FROM users) ORDER BY p.CreaionDate LIMIT 1
SELECT T2.DisplayName FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Name LIKE 'Autobiographer' ORDER BY T1.Date ASC LIMIT 1
SELECT COUNT(DISTINCT u.Id)  FROM users u  JOIN posts p ON u.Id = p.OwnerUserId  WHERE u.Location = 'United Kingdom' AND p.FavoriteCount >= 4
SELECT AVG(DISTINCT v.PostId) AS AverageNumberPostsVoted FROM votes v JOIN users u ON v.UserId = u.Id WHERE u.Age = (SELECT MAX(Age) FROM users)
SELECT DisplayName FROM users ORDER BY Reputation DESC LIMIT 1
SELECT COUNT(Id) FROM users WHERE Reputation > 2000 AND Views > 1000
SELECT DisplayName FROM users WHERE Age BETWEEN 19 AND 65
SELECT COUNT(*) FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Jay Stevens' AND STRFTIME('%Y', p.CreaionDate) = '2010'
SELECT p.Id, p.Title FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Harvey Motulsky' ORDER BY p.ViewCount DESC LIMIT 1
SELECT Id, Title FROM posts ORDER BY Score DESC LIMIT 1
SELECT AVG(p.Score) FROM users u JOIN posts p ON u.Id = p.OwnerUserId WHERE u.DisplayName = 'Stephen Turner'
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id WHERE T1.ViewCount > 20000 AND STRFTIME('%Y', T1.CreaionDate) = '2011'
SELECT Id, OwnerDisplayName  FROM posts  WHERE SUBSTR(CreaionDate, 1, 4) = '2010'  ORDER BY FavoriteCount DESC  LIMIT 1
SELECT CAST(COUNT(CASE WHEN u.Reputation > 1000 THEN 1 END) AS REAL) * 100 / COUNT(*) AS percentage FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE STRFTIME('%Y', p.CreaionDate) = '2011'
SELECT CAST(SUM(CASE WHEN Age BETWEEN 13 AND 18 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(Id) FROM users
SELECT p.ViewCount, u.DisplayName FROM posts p JOIN users u ON p.LastEditorUserId = u.Id WHERE p.Title = 'Computer game datasets'
SELECT COUNT(*) FROM posts WHERE ViewCount > (SELECT AVG(ViewCount) FROM posts)
SELECT COUNT(*) FROM comments WHERE PostId = (SELECT Id FROM posts ORDER BY Score DESC LIMIT 1)
SELECT COUNT(Id) FROM posts WHERE ViewCount > 35000 AND CommentCount = 0
SELECT u.DisplayName, u.Location FROM users u JOIN posts p ON u.Id = p.LastEditorUserId WHERE p.Id = 183
SELECT b.Name FROM badges b JOIN users u ON b.UserId = u.Id WHERE u.DisplayName = 'Emmett' ORDER BY b.Date DESC LIMIT 1
SELECT COUNT(*) FROM users WHERE Age BETWEEN 19 AND 65 AND UpVotes > 5000
SELECT strftime('%J', T1.Date) - strftime('%J', T2.CreationDate) AS DaysToGetBadge FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Zolomon'
SELECT (SELECT COUNT(*) FROM posts WHERE OwnerUserId = (SELECT Id FROM users ORDER BY CreationDate DESC LIMIT 1)) AS NumberOfPosts, (SELECT COUNT(*) FROM comments WHERE UserId = (SELECT Id FROM users ORDER BY CreationDate DESC LIMIT 1)) AS NumberOfComments
SELECT c.Text, c.UserDisplayName FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.Title = 'Analysing wind data with R' ORDER BY c.CreationDate DESC LIMIT 10
SELECT COUNT(DISTINCT UserId) FROM badges WHERE Name = 'Citizen Patrol'
SELECT COUNT(*) FROM posts JOIN tags ON posts.Tags LIKE '%' || tags.TagName || '%' WHERE tags.TagName = 'careers'
SELECT Reputation, Views FROM users WHERE DisplayName = 'Jarrod Dixon'
SELECT (SELECT COUNT(*) FROM comments WHERE PostId = (SELECT Id FROM posts WHERE Title = 'Clustering 1D data')) AS NumberOfComments, (SELECT COUNT(*) FROM posts WHERE ParentId = (SELECT Id FROM posts WHERE Title = 'Clustering 1D data') AND PostTypeId = 2) AS NumberOfAnswers
SELECT CreationDate FROM users WHERE DisplayName = 'IrishStat'
SELECT COUNT(*) FROM votes WHERE BountyAmount >= 30
SELECT CAST(COUNT(CASE WHEN p.Score > 50 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) AS percentage FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.Reputation = (SELECT MAX(Reputation) FROM users)
SELECT COUNT(*) FROM posts WHERE Score < 20
SELECT COUNT(Id) FROM tags WHERE Id < 15 AND Count <= 20
SELECT ExcerptPostId, WikiPostId FROM tags WHERE TagName = 'sample'
SELECT u.Reputation, u.UpVotes FROM comments c JOIN users u ON c.UserId = u.Id WHERE c.Text = 'fine, you win :)'
SELECT c.Text FROM posts p INNER JOIN comments c ON p.Id = c.PostId WHERE p.Title LIKE '%linear regression%'
SELECT c.Text FROM comments c JOIN posts p ON c.PostId = p.Id WHERE p.ViewCount BETWEEN 100 AND 150 ORDER BY c.Score DESC LIMIT 1
SELECT T2.CreationDate, T2.Age FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.WebsiteUrl LIKE 'http://%'
SELECT COUNT(DISTINCT p.Id) FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.ViewCount < 5 AND c.Score = 0
SELECT COUNT(*) FROM comments WHERE PostId IN (SELECT Id FROM posts WHERE CommentCount = 1) AND Score = 0
SELECT COUNT(DISTINCT users.Id) AS TotalNumberOfUsers FROM comments JOIN users ON comments.UserId = users.Id WHERE comments.Score = 0 AND users.Age = 40
SELECT p.Id, c.Text FROM posts p JOIN comments c ON p.Id = c.PostId WHERE p.Title = 'Group differences on a five point Likert item'
SELECT u.UpVotes FROM comments c JOIN users u ON c.UserId = u.Id WHERE c.Text = 'R is also lazy evaluated.'
SELECT T1.Text FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Harvey Motulsky'
SELECT T2.DisplayName FROM comments AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T1.Score BETWEEN 1 AND 5 AND T2.DownVotes = 0
SELECT CAST(SUM(CASE WHEN u.UpVotes = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM comments c JOIN users u ON c.UserId = u.Id WHERE c.Score BETWEEN 5 AND 10
SELECT sp.power_name FROM superhero AS h JOIN hero_power AS hp ON h.id = hp.hero_id JOIN superpower AS sp ON hp.power_id = sp.id WHERE h.superhero_name = '3-D Man'
SELECT COUNT(*) FROM superpower JOIN hero_power ON superpower.id = hero_power.power_id WHERE superpower.power_name = 'Super Strength'
SELECT COUNT(DISTINCT superhero.id) AS number_of_superheroes FROM superhero JOIN hero_power ON superhero.id = hero_power.hero_id JOIN superpower ON hero_power.power_id = superpower.id WHERE superpower.power_name = 'Super Strength' AND superhero.height_cm > 200
SELECT s.full_name FROM superhero s JOIN hero_power hp ON s.id = hp.hero_id GROUP BY s.id HAVING COUNT(hp.power_id) > 15
SELECT COUNT(*) FROM superhero sh JOIN colour c ON sh.eye_colour_id = c.id WHERE c.colour = 'Blue'
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.skin_colour_id = T2.id WHERE T1.superhero_name = 'Apocalypse'
SELECT COUNT(*) FROM superhero JOIN colour ON superhero.eye_colour_id = colour.id JOIN hero_power ON superhero.id = hero_power.hero_id JOIN superpower ON hero_power.power_id = superpower.id WHERE colour.colour = 'Blue' AND superpower.power_name = 'Agility'
SELECT s.superhero_name FROM superhero s JOIN colour c_eye ON s.eye_colour_id = c_eye.id AND c_eye.colour = 'Blue' JOIN colour c_hair ON s.hair_colour_id = c_hair.id AND c_hair.colour = 'Blond'
SELECT COUNT(*) FROM superhero JOIN publisher ON superhero.publisher_id = publisher.id WHERE publisher.publisher_name = 'Marvel Comics'
SELECT s.superhero_name FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'Marvel Comics' ORDER BY s.height_cm DESC
SELECT p.publisher_name FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE s.superhero_name = 'Sauron'
SELECT c.colour FROM superhero s JOIN publisher p ON s.publisher_id = p.id JOIN colour c ON s.eye_colour_id = c.id WHERE p.publisher_name = 'Marvel Comics' GROUP BY c.colour ORDER BY COUNT(s.id) DESC
SELECT AVG(s.height_cm) FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'Marvel Comics'
SELECT DISTINCT T1.superhero_name FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id INNER JOIN superpower AS T3 ON T2.power_id = T3.id INNER JOIN publisher AS T4 ON T1.publisher_id = T4.id WHERE T3.power_name = 'Super Strength' AND T4.publisher_name = 'Marvel Comics'
SELECT COUNT(*) FROM superhero JOIN publisher ON superhero.publisher_id = publisher.id WHERE publisher.publisher_name = 'DC Comics'
SELECT p.publisher_name FROM hero_attribute ha JOIN attribute a ON ha.attribute_id = a.id JOIN superhero s ON ha.hero_id = s.id JOIN publisher p ON s.publisher_id = p.id WHERE a.attribute_name = 'Speed' ORDER BY ha.attribute_value ASC LIMIT 1
SELECT COUNT(*) FROM superhero AS T1 JOIN colour AS T2 ON T1.eye_colour_id = T2.id JOIN publisher AS T3 ON T1.publisher_id = T3.id WHERE T2.colour = 'Gold' AND T3.publisher_name = 'Marvel Comics'
SELECT p.publisher_name FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE s.superhero_name = 'Blue Beetle II'
SELECT COUNT(*) FROM superhero sh JOIN colour c ON sh.hair_colour_id = c.id WHERE c.colour = 'Blond'
SELECT s.superhero_name FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Intelligence' ORDER BY ha.attribute_value ASC LIMIT 1
SELECT r.race FROM superhero s JOIN race r ON s.race_id = r.id WHERE s.superhero_name = 'Copycat'
SELECT s.superhero_name FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Durability' AND ha.attribute_value < 50
SELECT s.superhero_name FROM hero_power hp JOIN superpower sp ON hp.power_id = sp.id JOIN superhero s ON hp.hero_id = s.id WHERE sp.power_name = 'Death Touch'
SELECT COUNT(s.id) FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id JOIN gender g ON s.gender_id = g.id WHERE g.gender = 'Female' AND a.attribute_name = 'Strength' AND ha.attribute_value = 100
SELECT t1.superhero_name FROM superhero AS t1 JOIN hero_power AS t2 ON t1.id = t2.hero_id GROUP BY t1.superhero_name ORDER BY COUNT(t2.power_id) DESC LIMIT 1
SELECT COUNT(*) FROM superhero JOIN race ON superhero.race_id = race.id WHERE race.race = 'Vampire'
SELECT (CAST(SUM(CASE WHEN a.alignment = 'Bad' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(s.id)) AS percentage_bad, COUNT(CASE WHEN p.publisher_name = 'Marvel Comics' AND a.alignment = 'Bad' THEN 1 END) AS marvel_comics_bad_count FROM superhero s JOIN alignment a ON s.alignment_id = a.id JOIN publisher p ON s.publisher_id = p.id
SELECT (SELECT COUNT(*) FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'Marvel Comics') - (SELECT COUNT(*) FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'DC Comics') AS difference
SELECT id FROM publisher WHERE publisher_name = 'Star Trek'
SELECT AVG(attribute_value) FROM hero_attribute
SELECT COUNT(*) FROM superhero WHERE full_name IS NULL
SELECT c.colour FROM colour c JOIN superhero s ON c.id = s.eye_colour_id WHERE s.id = 75
SELECT sp.power_name FROM superhero sh JOIN hero_power hp ON sh.id = hp.hero_id JOIN superpower sp ON hp.power_id = sp.id WHERE sh.superhero_name = 'Deathlok'
SELECT AVG(superhero.weight_kg) FROM superhero JOIN gender ON superhero.gender_id = gender.id WHERE gender.gender = 'Female'
SELECT DISTINCT power_name FROM superhero JOIN gender ON superhero.gender_id = gender.id JOIN hero_power ON superhero.id = hero_power.hero_id JOIN superpower ON hero_power.power_id = superpower.id WHERE gender.gender = 'Male' LIMIT 5
SELECT s.superhero_name FROM superhero s JOIN race r ON s.race_id = r.id WHERE r.race = 'Alien'
SELECT superhero_name FROM superhero JOIN colour ON superhero.eye_colour_id = colour.id WHERE height_cm BETWEEN 170 AND 190 AND colour = 'No Colour'
SELECT T2.power_name FROM hero_power AS T1 INNER JOIN superpower AS T2 ON T1.power_id = T2.id WHERE T1.hero_id = 56
SELECT s.full_name FROM superhero s JOIN race r ON s.race_id = r.id WHERE r.race = 'Demi-God' LIMIT 5
SELECT COUNT(*) FROM alignment JOIN superhero ON alignment.id = superhero.alignment_id WHERE alignment.alignment = 'Bad'
SELECT race FROM race JOIN superhero ON race.id = superhero.race_id WHERE superhero.weight_kg = 169
SELECT c.colour FROM superhero s JOIN colour c ON s.hair_colour_id = c.id JOIN race r ON s.race_id = r.id WHERE s.height_cm = 185 AND r.race = 'Human'
SELECT DISTINCT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.weight_kg = ( SELECT MAX(T1.weight_kg) FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id )
SELECT (COUNT(CASE WHEN T2.publisher_name = 'Marvel Comics' THEN 1 ELSE NULL END) * 100.0 / COUNT(T2.publisher_name)) AS percentage FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.height_cm BETWEEN 150 AND 180
SELECT s.superhero_name FROM superhero s JOIN gender g ON s.gender_id = g.id WHERE g.gender = 'Male' AND s.weight_kg > (SELECT AVG(weight_kg) * 0.79 FROM superhero)
SELECT sp.power_name FROM superpower sp JOIN hero_power hp ON sp.id = hp.power_id GROUP BY sp.power_name ORDER BY COUNT(hp.hero_id) DESC LIMIT 1
SELECT ha.attribute_value FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE s.superhero_name = 'Abomination'
SELECT T1.power_name FROM superpower AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.power_id WHERE T2.hero_id = 1
SELECT COUNT(DISTINCT hp.hero_id) FROM hero_power hp JOIN superpower sp ON hp.power_id = sp.id WHERE sp.power_name = 'Stealth'
SELECT s.full_name FROM hero_attribute ha JOIN attribute a ON ha.attribute_id = a.id JOIN superhero s ON ha.hero_id = s.id WHERE a.attribute_name = 'Strength' ORDER BY ha.attribute_value DESC LIMIT 1
SELECT CAST(COUNT(T1.id) AS REAL) / SUM(CASE WHEN T2.colour = 'No Colour' THEN 1 ELSE 0 END) FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.skin_colour_id = T2.id
SELECT COUNT(*) FROM superhero h JOIN publisher p ON h.publisher_id = p.id WHERE p.publisher_name = 'Dark Horse Comics'
SELECT s.superhero_name FROM superhero s JOIN publisher p ON s.publisher_id = p.id JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE p.publisher_name = 'Dark Horse Comics' AND a.attribute_name = 'Durability' ORDER BY ha.attribute_value DESC LIMIT 1
SELECT c.colour FROM superhero s JOIN colour c ON s.eye_colour_id = c.id WHERE s.full_name = 'Abraham Sapien'
SELECT s.superhero_name FROM superhero s JOIN hero_power hp ON s.id = hp.hero_id JOIN superpower p ON hp.power_id = p.id WHERE p.power_name = 'Flight'
SELECT c1.colour AS eyes, c2.colour AS hair, c3.colour AS skin_colour FROM superhero h JOIN gender g ON h.gender_id = g.id JOIN publisher p ON h.publisher_id = p.id JOIN colour c1 ON h.eye_colour_id = c1.id JOIN colour c2 ON h.hair_colour_id = c2.id JOIN colour c3 ON h.skin_colour_id = c3.id WHERE g.gender = 'Female' AND p.publisher_name = 'Dark Horse Comics'
SELECT s.superhero_name, p.publisher_name FROM superhero s JOIN publisher p ON s.publisher_id = p.id WHERE s.eye_colour_id = s.hair_colour_id AND s.hair_colour_id = s.skin_colour_id
SELECT T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.superhero_name = 'A-Bomb'
SELECT CAST(SUM(CASE WHEN c.colour = 'Blue' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM superhero s JOIN gender g ON s.gender_id = g.id JOIN colour c ON s.skin_colour_id = c.id WHERE g.gender = 'Female'
SELECT T1.superhero_name, T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.full_name = 'Charles Chandler'
SELECT g.gender FROM superhero s JOIN gender g ON s.gender_id = g.id WHERE s.superhero_name = 'Agent 13'
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id INNER JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T3.power_name = 'Adaptation'
SELECT COUNT(*) FROM hero_power WHERE hero_id = (SELECT id FROM superhero WHERE superhero_name = 'Amazo')
SELECT sp.power_name FROM superhero s JOIN hero_power hp ON s.id = hp.hero_id JOIN superpower sp ON hp.power_id = sp.id WHERE s.full_name = 'Hunter Zolomon'
SELECT height_cm FROM superhero AS h JOIN colour AS c ON h.eye_colour_id = c.id WHERE c.colour = 'Amber'
SELECT s.superhero_name FROM superhero s JOIN colour c_eye ON s.eye_colour_id = c_eye.id JOIN colour c_hair ON s.hair_colour_id = c_hair.id WHERE c_eye.colour = 'Black' AND c_hair.colour = 'Black'
SELECT DISTINCT c2.colour AS eye_colour FROM superhero sh JOIN colour c1 ON sh.skin_colour_id = c1.id JOIN colour c2 ON sh.eye_colour_id = c2.id WHERE c1.colour = 'Gold'
SELECT s.full_name FROM superhero s JOIN race r ON s.race_id = r.id WHERE r.race = 'Vampire'
SELECT s.superhero_name FROM superhero s JOIN alignment a ON s.alignment_id = a.id WHERE a.alignment = 'Neutral'
SELECT COUNT(*) FROM hero_attribute ha JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Strength' AND ha.attribute_value = ( SELECT MAX(ha2.attribute_value) FROM hero_attribute ha2 JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Strength' )
SELECT r.race, a.alignment FROM superhero s JOIN race r ON s.race_id = r.id JOIN alignment a ON s.alignment_id = a.id WHERE s.superhero_name = 'Cameron Hicks'
SELECT CAST(SUM(CASE WHEN g.gender = 'Female' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS female_percentage FROM superhero h JOIN gender g ON h.gender_id = g.id JOIN publisher p ON h.publisher_id = p.id WHERE p.publisher_name = 'Marvel Comics'
SELECT AVG(s.weight_kg) AS average_weight FROM superhero s JOIN race r ON s.race_id = r.id WHERE r.race = 'Alien'
SELECT    (SELECT SUM(weight_kg) FROM superhero WHERE full_name = 'Emil Blonsky') -   (SELECT SUM(weight_kg) FROM superhero WHERE full_name = 'Charles Chandler') AS difference
SELECT AVG(height_cm) FROM superhero
SELECT sp.power_name FROM superhero AS h JOIN hero_power AS hp ON h.id = hp.hero_id JOIN superpower AS sp ON hp.power_id = sp.id WHERE h.superhero_name = 'Abomination'
SELECT COUNT(s.id) FROM superhero s INNER JOIN race r ON s.race_id = r.id INNER JOIN gender g ON s.gender_id = g.id WHERE r.id = 21 AND g.id = 1
SELECT s.superhero_name FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Speed' ORDER BY ha.attribute_value DESC LIMIT 1
SELECT COUNT(*) FROM superhero WHERE alignment_id = 3
SELECT a.attribute_name, ha.attribute_value FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE s.superhero_name = '3-D Man'
SELECT DISTINCT T1.superhero_name  FROM superhero AS T1  JOIN colour AS T2 ON T2.id = T1.eye_colour_id  JOIN colour AS T3 ON T3.id = T1.hair_colour_id WHERE T2.colour = 'Blue' AND T3.colour = 'Brown'
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T1.superhero_name IN ('Hawkman', 'Karate Kid', 'Speedy')
SELECT COUNT(*) FROM superhero WHERE publisher_id = 1
SELECT CAST(SUM(CASE WHEN c.colour = 'Blue' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(s.id) AS percentage FROM superhero s JOIN colour c ON s.eye_colour_id = c.id
SELECT CAST(SUM(CASE WHEN T2.gender = 'Male' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.gender = 'Female' THEN 1 ELSE 0 END) AS ratio FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id
SELECT superhero_name FROM superhero ORDER BY height_cm DESC LIMIT 1
SELECT id FROM superpower WHERE power_name = 'Cryokinesis'
SELECT superhero_name FROM superhero WHERE id = 294
SELECT full_name FROM superhero WHERE weight_kg = 0 OR weight_kg IS NULL
SELECT colour FROM colour JOIN superhero ON colour.id = superhero.eye_colour_id WHERE superhero.full_name = 'Karen Beecher-Duncan'
SELECT sp.power_name  FROM superhero h  JOIN hero_power hp ON h.id = hp.hero_id  JOIN superpower sp ON hp.power_id = sp.id  WHERE h.full_name = 'Helen Parr'
SELECT T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.height_cm = 188 AND T1.weight_kg = 108
SELECT publisher.publisher_name FROM superhero JOIN publisher ON superhero.publisher_id = publisher.id WHERE superhero.id = 38
SELECT T3.race FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id INNER JOIN race AS T3 ON T2.race_id = T3.id ORDER BY T1.attribute_value DESC LIMIT 1
SELECT a.alignment, sp.power_name FROM superhero h JOIN alignment a ON h.alignment_id = a.id JOIN hero_power hp ON h.id = hp.hero_id JOIN superpower sp ON hp.power_id = sp.id WHERE h.superhero_name = 'Atom IV'
SELECT s.full_name FROM superhero s JOIN colour c ON s.eye_colour_id = c.id WHERE c.colour = 'Blue' LIMIT 5
SELECT AVG(ha.attribute_value) FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id WHERE s.alignment_id = 3
SELECT DISTINCT T3.colour FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id INNER JOIN colour AS T3 ON T2.skin_colour_id = T3.id WHERE T1.attribute_value = 100
SELECT COUNT(*) FROM superhero s JOIN gender g ON s.gender_id = g.id JOIN alignment a ON s.alignment_id = a.id WHERE g.id = 2 AND a.id = 1
SELECT s.superhero_name FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id WHERE ha.attribute_value BETWEEN 75 AND 80
SELECT DISTINCT r.race FROM superhero s JOIN gender g ON s.gender_id = g.id JOIN colour c ON s.hair_colour_id = c.id JOIN race r ON s.race_id = r.id WHERE g.gender = 'Male' AND c.colour = 'Blue'
SELECT CAST(COUNT(CASE WHEN T2.id = 2 THEN 1 END) AS REAL) * 100 / COUNT(T1.id) FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id INNER JOIN alignment AS T3 ON T1.alignment_id = T3.id WHERE T3.id = 2
SELECT SUM(CASE WHEN T2.id = 7 THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.id = 1 THEN 1 ELSE 0 END) AS difference FROM superhero AS T1 JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.weight_kg = 0 OR T1.weight_kg IS NULL
SELECT attribute_value FROM hero_attribute WHERE hero_id = (SELECT id FROM superhero WHERE superhero_name = 'Hulk') AND attribute_id = (SELECT id FROM attribute WHERE attribute_name = 'Strength')
SELECT T3.power_name FROM superhero AS T1 JOIN hero_power AS T2 ON T1.id = T2.hero_id JOIN superpower AS T3 ON T2.power_id = T3.id WHERE T1.superhero_name = 'Ajax'
SELECT COUNT(*) FROM superhero s JOIN colour c ON s.skin_colour_id = c.id JOIN alignment a ON s.alignment_id = a.id WHERE c.colour = 'Green' AND a.alignment = 'Bad'
SELECT COUNT(T1.superhero_name) FROM superhero AS T1 JOIN gender AS T2 ON T1.gender_id = T2.id JOIN publisher AS T3 ON T1.publisher_id = T3.id WHERE T2.gender = 'Female' AND T3.publisher_name = 'Marvel Comics'
SELECT superhero_name FROM superhero JOIN hero_power ON superhero.id = hero_power.hero_id JOIN superpower ON hero_power.power_id = superpower.id WHERE superpower.power_name = 'Wind Control' ORDER BY superhero_name
SELECT g.gender FROM superhero AS h JOIN hero_power AS hp ON h.id = hp.hero_id JOIN superpower AS sp ON hp.power_id = sp.id JOIN gender AS g ON h.gender_id = g.id WHERE sp.power_name = 'Phoenix Force'
SELECT superhero_name FROM ( SELECT superhero_name, weight_kg FROM superhero JOIN publisher ON superhero.publisher_id = publisher.id WHERE publisher_name = 'DC Comics' ORDER BY weight_kg DESC LIMIT 1 ) AS heaviest_superhero
SELECT AVG(height_cm) FROM superhero JOIN race ON superhero.race_id = race.id JOIN publisher ON superhero.publisher_id = publisher.id WHERE race.race <> 'Human' AND publisher.publisher_name = 'Dark Horse Comics'
SELECT COUNT(DISTINCT ha.hero_id)  FROM hero_attribute ha  JOIN attribute a ON ha.attribute_id = a.id  WHERE a.attribute_name = 'Speed' AND ha.attribute_value = 100
SELECT SUM(CASE WHEN p.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN p.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS difference FROM superhero s JOIN publisher p ON s.publisher_id = p.id
SELECT a.attribute_name FROM attribute a JOIN hero_attribute ha ON a.id = ha.attribute_id JOIN superhero s ON ha.hero_id = s.id WHERE s.superhero_name = 'Black Panther' ORDER BY ha.attribute_value ASC LIMIT 1
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id WHERE T1.superhero_name = 'Abomination'
SELECT superhero_name FROM superhero ORDER BY height_cm DESC LIMIT 1
SELECT superhero_name FROM superhero WHERE full_name = 'Charles Chandler'
SELECT CAST(SUM(CASE WHEN g.gender = 'Female' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS female_percentage FROM superhero s JOIN gender g ON s.gender_id = g.id JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'George Lucas'
SELECT CAST(SUM(CASE WHEN T2.alignment = 'Good' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T3.publisher_name) FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id INNER JOIN publisher AS T3 ON T1.publisher_id = T3.id WHERE T3.publisher_name = 'Marvel Comics'
SELECT COUNT(*) FROM superhero WHERE full_name LIKE 'John%'
SELECT hero_id FROM hero_attribute WHERE attribute_value = (SELECT MIN(attribute_value) FROM hero_attribute)
SELECT full_name FROM superhero WHERE superhero_name = 'Alien'
SELECT superhero.full_name FROM superhero JOIN colour ON superhero.eye_colour_id = colour.id WHERE superhero.weight_kg < 100 AND colour.colour = 'Brown'
SELECT ha.attribute_value FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id WHERE s.superhero_name = 'Aquababy'
SELECT T1.weight_kg, T2.race FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T1.id = 40
SELECT AVG(s.height_cm) FROM superhero s JOIN alignment a ON s.alignment_id = a.id WHERE a.alignment = 'Neutral'
SELECT T2.hero_id FROM superpower AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.power_id INNER JOIN superhero AS T3 ON T2.hero_id = T3.id WHERE T1.power_name = 'Intelligence'
SELECT c.colour FROM superhero s JOIN colour c ON s.eye_colour_id = c.id WHERE s.superhero_name = 'Blackwulf'
SELECT DISTINCT sp.power_name FROM superpower sp JOIN hero_power hp ON sp.id = hp.power_id JOIN superhero h ON hp.hero_id = h.id WHERE h.height_cm > (SELECT AVG(height_cm) * 0.8 FROM superhero)
SELECT T1.driverRef FROM drivers AS T1 JOIN qualifying AS T2 ON T1.driverid = T2.driverid WHERE T2.raceid = 20 ORDER BY T2.q1 DESC LIMIT 5
SELECT D.surname  FROM qualifying Q  JOIN drivers D ON Q.driverId = D.driverId  WHERE Q.raceId = 19  ORDER BY Q.q2  LIMIT 1
SELECT DISTINCT T1.year FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.location = "Shanghai"
SELECT T1.url FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.name = 'Circuit de Barcelona-Catalunya'
SELECT T1.name FROM races AS T1 JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.country = "Germany"
SELECT position FROM constructorstandings WHERE constructorid = (SELECT constructorid FROM constructors WHERE name = 'Renault')
SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitid = c.circuitid WHERE r.year = 2010 AND c.country NOT IN ('Asia', 'Europe')
SELECT T1.name FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.country = 'Spain'
SELECT circuits.lat, circuits.lng FROM races JOIN circuits ON races.circuitId = circuits.circuitId WHERE races.name = 'Australian Grand Prix'
SELECT r.url FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE c.name = 'Sepang International Circuit'
SELECT T1.time FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.name = 'Sepang International Circuit'
SELECT T2.lat, T2.lng FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T1.name = 'Abu Dhabi Grand Prix'
SELECT c.nationality FROM constructorResults cr JOIN constructors c ON cr.constructorId = c.constructorId WHERE cr.raceId = 24 AND cr.points = 1
SELECT q1 FROM qualifying q JOIN drivers d ON q.driverId = d.driverId WHERE d.forename = 'Bruno' AND d.surname = 'Senna' AND q.raceId = 354
SELECT T1.nationality FROM drivers AS T1 JOIN qualifying AS T2 ON T1.driverid = T2.driverid WHERE T2.raceid = 355 AND T2.q2 = "0:01:40"
SELECT number FROM qualifying WHERE q3 LIKE '1:54%' AND raceId = 903
SELECT COUNT(*) FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.name = 'Bahrain Grand Prix' AND ra.`year` = 2007 AND r.time IS NULL
SELECT T1.url FROM seasons AS T1 JOIN races AS T2 ON T1.year = T2.year WHERE T2.raceId = 901
SELECT COUNT(*) FROM races JOIN results ON races.raceId = results.raceId WHERE races.date = '2015-11-29' AND results.time IS NOT NULL
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN results AS T2 ON T1.driverid = T2.driverid WHERE T2.raceid = 592 AND T2.time IS NOT NULL ORDER BY T1.dob ASC LIMIT 1
SELECT d.url FROM drivers d JOIN laptimes l ON d.driverId = l.driverId WHERE l.raceId = 161 AND l.time LIKE '1:27%'
SELECT d.nationality FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE r.raceId = 933 ORDER BY r.fastestLapSpeed DESC LIMIT 1
SELECT T1.lat, T1.lng FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitid = T2.circuitid WHERE T2.name = 'Malaysian Grand Prix'
SELECT T2.url FROM constructorResults AS T1 INNER JOIN constructors AS T2 ON T1.constructorid = T2.constructorid WHERE T1.raceid = 9 ORDER BY T1.points DESC LIMIT 1
SELECT q.q1 FROM qualifying q JOIN drivers d ON q.driverId = d.driverId WHERE q.raceId = 345 AND d.forename = 'Lucas' AND d.surname = 'di Grassi'
SELECT T1.nationality FROM drivers AS T1 INNER JOIN qualifying AS T2 ON T1.driverId = T2.driverId WHERE T2.raceid = 347 AND T2.q2 LIKE '0:01:15'
SELECT D.code FROM qualifying Q JOIN drivers D ON Q.driverId = D.driverId WHERE Q.raceId = 45 AND Q.q3 LIKE '1:33%'
SELECT T1.time FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T2.forename = 'Bruce' AND T2.surname = 'McLaren' AND T1.raceId = 743
SELECT T3.forename, T3.surname FROM results AS T1 INNER JOIN races AS T2 ON T1.raceid = T2.raceid INNER JOIN drivers AS T3 ON T1.driverid = T3.driverid WHERE T2.name = 'San Marino Grand Prix' AND T2.year = 2006 AND T1.position = 2
SELECT T2.url FROM races AS T1 INNER JOIN seasons AS T2 ON T1.year = T2.year WHERE T1.raceId = 901
SELECT COUNT(CASE WHEN T2.statusId != 1 THEN 1 END) AS non_finishers_count FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId WHERE T1.date = '2015-11-29'
SELECT d.forename, d.surname FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE r.raceId = 872 AND r.time IS NOT NULL ORDER BY d.dob DESC LIMIT 1
SELECT d.forename, d.surname FROM laptimes l JOIN drivers d ON l.driverId = d.driverId WHERE l.raceId = 348 AND l.time = (SELECT MIN(time) FROM laptimes WHERE raceId = 348)
SELECT DISTINCT T2.nationality FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.fastestLapSpeed = ( SELECT MAX(fastestLapSpeed) FROM results )
SELECT ((r1.fastestLapSpeed - r2.fastestLapSpeed) / r1.fastestLapSpeed) * 100 AS percentage_difference FROM results r1 JOIN results r2 ON r1.driverId = r2.driverId WHERE r1.raceId = 853 AND r2.raceId = 854 AND r1.driverId = (SELECT driverId FROM drivers WHERE forename = 'Paul' AND surname = 'di Resta')
SELECT (COUNT(CASE WHEN r.time IS NOT NULL THEN 1 END) * 100.0 / COUNT(r.driverId)) AS completion_rate FROM races ra JOIN results r ON ra.raceId = r.raceId WHERE ra.date = '1983-07-16'
SELECT `year` FROM races WHERE name = 'Singapore Grand Prix' ORDER BY `year` ASC LIMIT 1
SELECT COUNT(*) AS number_of_races, name FROM races WHERE year = 2005 ORDER BY name DESC
SELECT name FROM races WHERE strftime('%Y-%m', date) =  (SELECT strftime('%Y-%m', MIN(date)) FROM races)
SELECT name, date FROM races WHERE `year` = 1999 AND round = (SELECT MAX(round) FROM races WHERE `year` = 1999)
SELECT `year` FROM races GROUP BY `year` ORDER BY COUNT(*) DESC LIMIT 1
SELECT name FROM races WHERE year = 2017 EXCEPT SELECT name FROM races WHERE year = 2000
SELECT c.country, c.name, c.location FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name = 'European Grand Prix' ORDER BY r.year ASC LIMIT 1
SELECT MAX(r.year) FROM races r JOIN circuits c ON r.circuitid = c.circuitid WHERE c.name = 'Brands Hatch' AND r.name = 'British Grand Prix'
SELECT COUNT(DISTINCT T2.year) FROM circuits AS T1  INNER JOIN races AS T2 ON T1.circuitid = T2.circuitid  WHERE T2.name = 'British Grand Prix' AND T1.name = 'Silverstone Circuit'
SELECT T3.forename, T3.surname FROM results AS T1 INNER JOIN races AS T2 ON T1.raceid = T2.raceid INNER JOIN drivers AS T3 ON T1.driverid = T3.driverid WHERE T2.name = 'Singapore Grand Prix' AND T2.year = 2010 ORDER BY T1.position
SELECT d.forename, d.surname, SUM(ds.points) AS total_points FROM drivers d JOIN driverstandings ds ON d.driverid = ds.driverid GROUP BY ds.driverid HAVING total_points = (     SELECT MAX(total_points) FROM (         SELECT SUM(points) AS total_points FROM driverStandings GROUP BY driverid     ) AS subquery )
SELECT T1.forename, T1.surname, T2.points FROM drivers AS T1 JOIN results AS T2 ON T1.driverid = T2.driverid JOIN races AS T3 ON T2.raceid = T3.raceid WHERE T3.name = "Chinese Grand Prix" AND T3.year = 2017 ORDER BY T2.points DESC LIMIT 3
SELECT d.forename, d.surname, r.name FROM laptimes l JOIN drivers d ON l.driverId = d.driverId JOIN races r ON l.raceId = r.raceId WHERE l.milliseconds = (SELECT MIN(milliseconds) FROM laptimes)
SELECT AVG(lt.milliseconds) AS average_lap_time FROM laptimes lt JOIN races r ON lt.raceId = r.raceId JOIN drivers d ON lt.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' AND r.name = 'Malaysian Grand Prix' AND r.year = 2009
SELECT (CAST(count_not_first_position AS REAL) / total_races) * 100 AS percentage_not_first_position FROM ( SELECT COUNT(*) AS count_not_first_position FROM results r JOIN races rs ON r.raceId = rs.raceId JOIN drivers d ON r.driverId = d.driverId WHERE rs.year >= 2010 AND d.surname = 'Hamilton' AND r.position > 1 ) AS not_first JOIN ( SELECT COUNT(*) AS total_races FROM results r JOIN races rs ON r.raceId = rs.raceId JOIN drivers d ON r.driverId = d.driverId WHERE rs.year >= 2010 AND d.surname = 'Hamilton' ) AS total
SELECT T1.forename, T1.surname, T1.nationality, MAX(T2.points) FROM drivers AS T1 JOIN driverStandings AS T2 ON T1.driverid = T2.driverid GROUP BY T1.driverid ORDER BY SUM(T2.wins) DESC LIMIT 1
SELECT (STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', dob)) AS age, forename, surname FROM drivers WHERE nationality = 'Japanese' ORDER BY dob DESC LIMIT 1
SELECT c.name FROM circuits c JOIN races r ON c.circuitId = r.circuitId WHERE r.year BETWEEN 1990 AND 2000 GROUP BY c.name HAVING COUNT(r.raceId) = 4
SELECT T1.name, T1.location, T2.name FROM circuits AS T1 INNER JOIN races AS T2 ON T1.circuitid = T2.circuitid WHERE T1.country = 'USA' AND T2.year = 2006
SELECT T1.name, T2.name, T2.location FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE strftime('%Y-%m', T1.`date`) = '2005-09'
SELECT r.name FROM races r JOIN driverStandings ds ON r.raceId = ds.raceId JOIN drivers d ON ds.driverId = d.driverId WHERE d.forename = 'Alex' AND d.surname = 'Yoong' AND ds.position < 20
SELECT COUNT(*) FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN circuits c ON ra.circuitId = c.circuitId JOIN drivers d ON r.driverId = d.driverId WHERE c.name = 'Sepang International Circuit' AND d.forename = 'Michael' AND d.surname = 'Schumacher' AND r.position = 1
SELECT r.name, r.year FROM laptimes l JOIN drivers d ON l.driverid = d.driverid JOIN races r ON l.raceid = r.raceid WHERE d.forename = 'Michael' AND d.surname = 'Schumacher' ORDER BY l.milliseconds LIMIT 1
SELECT AVG(r.points) AS average_points FROM results r JOIN drivers d ON r.driverId = d.driverId JOIN races ra ON r.raceId = ra.raceId WHERE d.forename = 'Eddie' AND d.surname = 'Irvine' AND ra.year = 2000
SELECT T1.name, T2.points FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T1.year LIMIT 1
SELECT r.name, c.country FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.year = 2017 ORDER BY r.date
SELECT r.name, r.year, c.location FROM races r JOIN results res ON r.raceId = res.raceId JOIN circuits c ON r.circuitId = c.circuitId ORDER BY res.laps DESC LIMIT 1
SELECT (SUM(CASE WHEN T2.country = 'Germany' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T1.name = 'European Grand Prix'
SELECT lat, lng FROM circuits WHERE name = 'Silverstone Circuit'
SELECT name FROM circuits WHERE name IN ('Silverstone Circuit', 'Hockenheimring', 'Hungaroring') ORDER BY lat DESC LIMIT 1
SELECT circuitRef FROM circuits WHERE name = 'Marina Bay Street Circuit'
SELECT country FROM circuits ORDER BY alt DESC LIMIT 1
SELECT COUNT(*) FROM drivers WHERE code IS NULL OR code = ''
SELECT nationality FROM drivers ORDER BY dob ASC LIMIT 1
SELECT surname FROM drivers WHERE nationality = 'Italian'
SELECT url FROM drivers WHERE forename = 'Anthony' AND surname = 'Davidson'
SELECT driverRef FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton'
SELECT c.name FROM circuits c JOIN races r ON c.circuitId = r.circuitId WHERE r.year = 2009 AND r.name = 'Spanish Grand Prix'
SELECT DISTINCT T1.year FROM races AS T1 JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.name = 'Silverstone Circuit'
SELECT R.url FROM races R JOIN circuits C ON R.circuitId = C.circuitId WHERE C.name = 'Silverstone Circuit'
SELECT T1.time FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T2.name = 'Yas Marina Circuit' AND T1.year = 2010
SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitid = c.circuitid WHERE c.country = 'Italy'
SELECT r.date FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE c.name = 'Sepang International Circuit'
SELECT T2.url FROM races AS T1 INNER JOIN circuits AS T2 ON T1.circuitid = T2.circuitid WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009
SELECT MIN(r.fastestLapTime) AS fastest_lap_time_ever FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
SELECT driverRef FROM drivers WHERE driverId = (SELECT driverId FROM results WHERE raceId = (SELECT raceId FROM races WHERE name = 'Canadian Grand Prix' AND YEAR = 2007) AND positionOrder = 1)
SELECT DISTINCT T3.name FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceId = T3.raceId WHERE T2.forename = "Lewis" AND T2.surname = "Hamilton"
SELECT r.name FROM races r JOIN results res ON r.raceId = res.raceId JOIN drivers d ON res.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' ORDER BY res.rank LIMIT 1
SELECT MAX(T2.fastestLapSpeed) FROM races AS T1 JOIN results AS T2 ON T1.raceid = T2.raceid WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009
SELECT DISTINCT r.year FROM results res JOIN races r ON res.raceId = r.raceId WHERE res.driverId = (SELECT driverId FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton')
SELECT T1.positionOrder FROM results AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId JOIN drivers AS T3 ON T1.driverId = T3.driverId WHERE T2.name = 'Chinese Grand Prix' AND T2.year = 2008 AND T3.forename = 'Lewis' AND T3.surname = 'Hamilton'
SELECT d.forename, d.surname FROM races r JOIN results res ON r.raceId = res.raceId JOIN drivers d ON res.driverId = d.driverId WHERE r.name = 'Australian Grand Prix' AND r.year = 1989 AND res.grid = 4
SELECT COUNT(*) FROM results WHERE raceId = (SELECT raceId FROM races WHERE name = 'Australian Grand Prix' AND year = 2008) AND time IS NOT NULL
SELECT r.fastestLapTime FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.name = 'Australian Grand Prix' AND ra.year = 2008 AND d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT r.time FROM races ra JOIN results r ON ra.raceId = r.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.name = 'Chinese Grand Prix' AND ra.year = 2008 AND r.position = 2
SELECT T3.forename, T3.surname, T3.url FROM races AS T1 INNER JOIN results AS T2 ON T1.raceid = T2.raceid INNER JOIN drivers AS T3 ON T2.driverid = T3.driverid WHERE T1.name = 'Australian Grand Prix' AND T1.year = 2008 AND T2.position = 1
SELECT COUNT(DISTINCT d.driverId) FROM drivers d JOIN results r ON d.driverId = r.driverId JOIN races ra ON r.raceId = ra.raceId WHERE d.nationality = 'British' AND ra.year = 2008 AND ra.name = 'Australian Grand Prix'
SELECT COUNT(DISTINCT T1.driverId) FROM results AS T1 JOIN races AS T2 ON T1.raceid = T2.raceid WHERE T2.name = 'Chinese Grand Prix' AND T2.year = 2008 AND T1.time IS NOT NULL
SELECT SUM(r.points) AS total_points FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT AVG( CAST(SUBSTR(r.fastestLapTime, 1, INSTR(r.fastestLapTime, ':') - 1) AS REAL) * 60 + CAST(SUBSTR(r.fastestLapTime, INSTR(r.fastestLapTime, ':') + 1, INSTR(r.fastestLapTime, '.') - INSTR(r.fastestLapTime, ':') - 1) AS REAL) + CAST(SUBSTR(r.fastestLapTime, INSTR(r.fastestLapTime, '.') + 1) AS REAL) / 1000) AS average_fastest_lap_time_seconds FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT CAST(COUNT(CASE WHEN r.time IS NOT NULL THEN 1 END) AS REAL) / COUNT(r.resultId) AS completion_rate FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.name = 'Australian Grand Prix' AND ra.year = 2008
SELECT      ((MAX(r1.milliseconds) - MIN(r1.milliseconds)) / MAX(r1.milliseconds)) * 100 AS percentage_faster FROM      races r JOIN      results r1 ON r.raceId = r1.raceId JOIN      drivers d1 ON r1.driverId = d1.driverId WHERE      r.name = 'Australian Grand Prix' AND r.year = 2008 AND r1.time IS NOT NULL
SELECT COUNT(circuitId) FROM circuits WHERE location = 'Adelaide' AND country = 'Australia'
SELECT lat, lng FROM circuits WHERE country = 'USA'
SELECT COUNT(*) FROM drivers WHERE nationality = 'British' AND dob > '1980-12-31'
SELECT MAX(cs.points) AS max_points FROM constructors c JOIN constructorStandings cs ON c.constructorId = cs.constructorId WHERE c.nationality = 'British'
SELECT T1.name FROM constructors AS T1 JOIN constructorStandings AS T2 ON T1.constructorid = T2.constructorid GROUP BY T1.constructorid ORDER BY sum(T2.points) DESC LIMIT 1
SELECT T2.name FROM constructorstandings AS T1 JOIN constructors AS T2 ON T1.constructorid = T2.constructorid WHERE T1.raceid = 291 AND T1.points = 0
SELECT COUNT(DISTINCT cs.constructorId) AS JapaneseConstructorsWith0PointsIn2Races FROM constructors c JOIN constructorStandings cs ON c.constructorId = cs.constructorId WHERE c.nationality = 'Japanese' GROUP BY cs.constructorId HAVING COUNT(cs.raceId) = 2 AND SUM(cs.points) = 0
SELECT DISTINCT T1.name FROM constructors AS T1 INNER JOIN constructorStandings AS T2 ON T1.constructorid = T2.constructorid WHERE T2.position = 1
SELECT COUNT(DISTINCT c.constructorId) AS FrenchConstructorsWithLapsOver50 FROM constructors c JOIN constructorStandings cs ON c.constructorId = cs.constructorId JOIN results r ON cs.raceId = r.raceId WHERE c.nationality = 'French' AND r.laps > 50
SELECT CAST(SUM(CASE WHEN r.time IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS completion_percentage FROM results r JOIN drivers d ON r.driverId = d.driverId JOIN races ra ON r.raceId = ra.raceId WHERE ra.year BETWEEN 2007 AND 2009 AND d.nationality = 'Japanese'
SELECT s.year, AVG(CAST(strftime('%s', r.time) - strftime('%s', '00:00:00') AS REAL)) AS avg_time_in_seconds FROM drivers d JOIN results r ON d.driverId = r.driverId JOIN races ra ON r.raceId = ra.raceId JOIN seasons s ON ra.year = s.year WHERE s.year < 1975 AND r.position = 1 GROUP BY s.year
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverid = T2.driverid WHERE T1.dob > '1975-12-31' AND T2.rank = 2
SELECT COUNT(*) FROM drivers d JOIN results r ON d.driverId = r.driverId WHERE d.nationality = 'Italian' AND r.time IS NULL
SELECT d.forename, d.surname FROM drivers d JOIN laptimes l ON d.driverId = l.driverId ORDER BY l.milliseconds ASC LIMIT 1
SELECT MIN(lap) AS fastest_lap_number FROM laptimes WHERE driverId = ( SELECT driverId FROM driverStandings WHERE raceId IN ( SELECT raceId FROM races WHERE year = 2009 ) GROUP BY driverId ORDER BY SUM(points) DESC LIMIT 1 )
SELECT AVG(r.fastestLapSpeed) AS average_fastest_lap_speed FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.name = 'Spanish Grand Prix' AND ra.year = 2009
SELECT r.name, r.year FROM races r JOIN results rs ON r.raceId = rs.raceId WHERE rs.milliseconds = ( SELECT MIN(milliseconds) FROM results WHERE milliseconds IS NOT NULL )
SELECT CAST(COUNT(CASE WHEN d.dob < '1985-01-01' AND r.laps > 50 THEN 1 END) AS REAL) * 100 / COUNT(d.driverId) AS percentage FROM drivers d JOIN results r ON d.driverId = r.driverId JOIN races ra ON r.raceId = ra.raceId WHERE ra.year BETWEEN 2000 AND 2005
SELECT COUNT(DISTINCT d.driverId) AS french_drivers_with_fast_laptime FROM drivers d JOIN laptimes l ON d.driverId = l.driverId WHERE d.nationality = 'French' AND CAST(SUBSTR(l.time, INSTR(l.time, ':') + 1) AS REAL) + 60 * CAST(SUBSTR(l.time, 1, INSTR(l.time, ':') - 1) AS REAL) < 120
SELECT code FROM drivers WHERE nationality = 'American'
SELECT raceId FROM races WHERE year = 2009
SELECT COUNT(DISTINCT driverId) FROM results WHERE raceId = 18
SELECT d.code, SUM(CASE WHEN d.nationality = 'Dutch' THEN 1 ELSE 0 END) AS DutchCount FROM drivers d ORDER BY d.dob ASC LIMIT 3
SELECT driverRef FROM drivers WHERE forename = 'Robert' AND surname = 'Kubica'
SELECT COUNT(*) FROM drivers WHERE strftime('%Y', dob) = '1980' AND nationality = 'British'
SELECT d.forename, d.surname FROM drivers d JOIN laptimes l ON d.driverId = l.driverId WHERE d.nationality = 'German' AND d.dob BETWEEN '1980-01-01' AND '1990-12-31' ORDER BY l.time ASC LIMIT 3
SELECT driverRef FROM drivers WHERE nationality = 'German' ORDER BY dob ASC LIMIT 1
SELECT T1.driverid, T1.code FROM drivers AS T1 JOIN results AS T2 ON T1.driverid = T2.driverid WHERE STRFTIME('%Y', T1.dob) = "1971" AND T2.fastestLapTime IS NOT NULL
SELECT d.forename, d.surname, MAX(lt.time) AS latest_lap_time FROM drivers d JOIN laptimes lt ON d.driverid = lt.driverid WHERE d.nationality = 'Spanish' AND d.dob < '1982-01-01' GROUP BY d.forename, d.surname ORDER BY latest_lap_time DESC LIMIT 10
SELECT r.year  FROM results res  JOIN races r ON res.raceId = r.raceId  ORDER BY res.fastestLapTime ASC  LIMIT 1
SELECT r.year FROM circuits c JOIN races r ON c.circuitId = r.circuitId JOIN laptimes l ON r.raceId = l.raceId ORDER BY l.time DESC LIMIT 1
SELECT driverId FROM lapTimes WHERE lap = 1 ORDER BY time ASC LIMIT 5
SELECT COUNT(driverId) FROM results WHERE raceId > 50 AND raceId < 100 AND time IS NOT NULL AND statusId = 2
SELECT location, lat, lng FROM circuits WHERE country = 'Austria'
SELECT raceId FROM results WHERE time IS NOT NULL GROUP BY raceId ORDER BY COUNT(*) DESC LIMIT 1
SELECT d.driverRef, d.nationality, d.dob  FROM qualifying q  JOIN drivers d ON q.driverId = d.driverId  WHERE q.raceId = 23 AND q.q2 IS NOT NULL
SELECT s.year, r.name, r.date, r.time FROM qualifying q JOIN drivers d ON q.driverid = d.driverid JOIN races r ON q.raceid = r.raceid JOIN seasons s ON r.year = s.year ORDER BY d.dob DESC, r.date ASC LIMIT 1
SELECT COUNT(DISTINCT d.driverId)  FROM drivers d  JOIN results r ON d.driverId = r.driverId  JOIN status s ON r.statusId = s.statusId  WHERE s.status = 'Puncture' AND d.nationality = 'American'
SELECT c.url FROM constructors c JOIN constructorStandings cs ON c.constructorId = cs.constructorId WHERE c.nationality = 'Italian' GROUP BY c.constructorId ORDER BY SUM(cs.points) DESC LIMIT 1
SELECT c.url FROM constructors c JOIN constructorstandings cs ON c.constructorid = cs.constructorid GROUP BY c.constructorid ORDER BY SUM(cs.wins) DESC LIMIT 1
SELECT d.forename, d.surname FROM drivers d JOIN lapTimes lt ON d.driverId = lt.driverId JOIN races r ON lt.raceId = r.raceId WHERE r.name = 'French Grand Prix' AND lt.lap = 3 ORDER BY lt.milliseconds DESC LIMIT 1
SELECT T2.name, T1.milliseconds FROM laptimes AS T1 JOIN races AS T2 ON T1.raceid = T2.raceid WHERE T1.lap = 1 ORDER BY T1.milliseconds LIMIT 1
SELECT AVG(r.fastestLapTime) AS average_fastest_lap_time FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.name = 'United States Grand Prix' AND ra.year = 2006 AND r.rank < 11
SELECT d.forename, d.surname FROM drivers d JOIN pitStops ps ON d.driverId = ps.driverId JOIN races r ON ps.raceId = r.raceId JOIN results rs ON r.raceId = rs.raceId WHERE d.nationality = 'German' AND d.dob BETWEEN '1980-01-01' AND '1985-12-31' GROUP BY d.driverId ORDER BY AVG(ps.duration) ASC LIMIT 3
SELECT d.forename, d.surname, r.time FROM drivers d JOIN results r ON d.driverId = r.driverId JOIN races ra ON r.raceId = ra.raceId WHERE ra.name = 'Canadian Grand Prix' AND ra.year = 2008 AND r.position = 1
SELECT c.constructorRef, c.url  FROM constructorStandings cs  JOIN races r ON cs.raceId = r.raceId  JOIN constructors c ON cs.constructorId = c.constructorId  WHERE r.year = 2009 AND r.name = 'Singapore Grand Prix'  ORDER BY cs.points DESC  LIMIT 1
SELECT forename, surname, dob FROM drivers WHERE nationality = 'Austrian' AND STRFTIME('%Y', dob) BETWEEN '1981' AND '1991'
SELECT forename || ' ' || surname AS full_name, url, dob FROM drivers WHERE nationality = 'German' AND dob BETWEEN '1971-01-01' AND '1985-12-31' ORDER BY dob DESC
SELECT location, country, lat, lng FROM circuits WHERE name = 'Hungaroring'
SELECT SUM(cst.points) AS total_points, c.name AS constructor_name, c.nationality AS constructor_nationality FROM races r JOIN constructorStandings cst ON r.raceId = cst.raceId JOIN constructors c ON cst.constructorId = c.constructorId WHERE r.name = 'Monaco Grand Prix' AND r.year BETWEEN 1980 AND 2010 GROUP BY c.constructorId ORDER BY total_points DESC LIMIT 1
SELECT AVG(r.points) AS average_score FROM races ra JOIN results r ON ra.raceId = r.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.name = 'Turkish Grand Prix' AND d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT AVG(race_count) AS annual_average_races FROM (     SELECT `year`, COUNT(raceId) AS race_count FROM races WHERE `date` BETWEEN '2000-01-01' AND '2010-12-31' GROUP BY `year` )
SELECT nationality FROM drivers GROUP BY nationality ORDER BY COUNT(*) DESC LIMIT 1
SELECT wins FROM driverStandings WHERE points = 91
SELECT T3.name FROM results AS T1 INNER JOIN laptimes AS T2 ON T1.raceId = T2.raceId INNER JOIN races AS T3 ON T1.raceId = T3.raceId GROUP BY T1.fastestLapTime ORDER BY T1.fastestLapTime ASC LIMIT 1
SELECT T1.location || ', ' || T1.country AS full_location FROM circuits AS T1 JOIN races AS T2 ON T1.circuitid = T2.circuitid ORDER BY T2.date DESC LIMIT 1
SELECT d.forename, d.surname FROM circuits c JOIN races r ON c.circuitId = r.circuitId JOIN qualifying q ON r.raceId = q.raceId JOIN drivers d ON q.driverId = d.driverId WHERE c.name = 'Marina Bay Street Circuit' AND r.year = 2008 AND q.position = 1 AND q.q3 = (SELECT MIN(q3) FROM qualifying WHERE raceId = r.raceId) ORDER BY q.position LIMIT 1
SELECT d.forename || ' ' || d.surname AS full_name, d.nationality, r.name AS first_race FROM drivers d JOIN results rs ON d.driverId = rs.driverId JOIN races r ON rs.raceId = r.raceId ORDER BY d.dob DESC LIMIT 1
SELECT COUNT(T3.statusId) FROM races AS T1 INNER JOIN results AS T2 ON T1.raceid = T2.raceid INNER JOIN status AS T3 ON T2.statusid = T3.statusid WHERE T1.name = 'Canadian Grand Prix' AND T3.status = 'Accident' GROUP BY T2.driverid ORDER BY COUNT(T3.statusId) DESC LIMIT 1
SELECT SUM(ds.wins) AS total_wins, d.forename, d.surname FROM drivers d JOIN driverStandings ds ON d.driverId = ds.driverId WHERE d.dob = (SELECT MIN(dob) FROM drivers) GROUP BY d.forename, d.surname
SELECT MAX(duration) FROM pitStops
SELECT time FROM laptimes ORDER BY time ASC LIMIT 1
SELECT MAX(T1.duration) FROM pitStops AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T2.forename = 'Lewis' AND T2.surname = 'Hamilton'
SELECT T3.lap FROM races AS T1 INNER JOIN drivers AS T2 ON T1.name = 'Australian Grand Prix' INNER JOIN pitstops AS T3 ON T1.raceid = T3.raceid INNER JOIN drivers AS T4 ON T3.driverid = T4.driverid WHERE T1.year = 2011 AND T4.forename = 'Lewis' AND T4.surname = 'Hamilton'
SELECT T2.duration FROM races AS T1 JOIN pitstops AS T2 ON T1.raceid = T2.raceid JOIN drivers AS T3 ON T2.driverid = T3.driverid WHERE T1.name = "Australian Grand Prix" AND YEAR = 2011
SELECT MIN(t.time) AS lap_record FROM drivers d JOIN laptimes t ON d.driverId = t.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT d.forename, d.surname FROM laptimes l JOIN drivers d ON l.driverId = d.driverId ORDER BY l.time ASC LIMIT 20
SELECT c.location FROM circuits c JOIN races r ON c.circuitId = r.circuitId JOIN results res ON r.raceId = res.raceId JOIN drivers d ON res.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' ORDER BY res.fastestLapTime ASC LIMIT 1
SELECT MIN(lt.time) FROM laptimes lt JOIN races r ON lt.raceId = r.raceId WHERE r.name = 'Austrian Grand Prix'
SELECT c.name AS circuit_name, MIN(lt.time) AS fastest_lap_time FROM circuits c JOIN races r ON c.circuitId = r.circuitId JOIN laptimes lt ON r.raceId = lt.raceId WHERE c.country = 'Italy' GROUP BY c.name
SELECT r.name FROM races r JOIN laptimes l ON r.raceId = l.raceId WHERE r.name = 'Austrian Grand Prix' ORDER BY l.time ASC LIMIT 1
SELECT SUM(ps.duration) AS total_pitstop_time FROM races r JOIN circuits c ON r.circuitid = c.circuitid JOIN laptimes lt ON r.raceid = lt.raceid JOIN pitstops ps ON r.raceid = ps.raceid AND lt.driverid = ps.driverid WHERE c.name = 'Austrian Grand Prix' AND lt.position = 1
SELECT c.lat, c.lng FROM circuits c JOIN races r ON c.circuitId = r.circuitId JOIN laptimes l ON r.raceId = l.raceId WHERE l.time = '1:29.488'
SELECT AVG(p.milliseconds) FROM pitStops p JOIN drivers d ON p.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton'
SELECT AVG(l.milliseconds) AS average FROM laptimes l JOIN races r ON l.raceid = r.raceid JOIN circuits c ON r.circuitid = c.circuitid WHERE c.country = 'Italy'
SELECT player_api_id FROM Player_Attributes WHERE overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
SELECT player_name, height FROM Player WHERE height = (SELECT MAX(height) FROM Player)
SELECT preferred_foot FROM Player_Attributes WHERE potential = (SELECT MIN(potential) FROM Player_Attributes)
SELECT COUNT(*) FROM Player_Attributes WHERE overall_rating >= 60 AND overall_rating < 65 AND defensive_work_rate = 'low'
SELECT DISTINCT player_api_id FROM Player_Attributes ORDER BY crossing DESC LIMIT 5
SELECT L.name FROM ( SELECT T.league_id, SUM(T.home_team_goal + T.away_team_goal) AS total_goals FROM Match T WHERE T.season = '2015/2016' GROUP BY T.league_id ORDER BY total_goals DESC LIMIT 1 ) AS Subquery JOIN League L ON Subquery.league_id = L.id
SELECT T2.team_long_name FROM Match AS T1 JOIN Team AS T2 ON T1.home_team_api_id = T2.team_api_id WHERE T1.season = '2015/2016' AND T1.home_team_goal < T1.away_team_goal GROUP BY T1.home_team_api_id ORDER BY COUNT(T1.id) ASC LIMIT 1
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.penalties DESC LIMIT 10
SELECT T.team_long_name FROM Team AS T JOIN Match AS M ON T.team_api_id = M.away_team_api_id JOIN League AS L ON M.league_id = L.id WHERE L.name = 'Scotland Premier League' AND M.season = '2009/2010' AND M.away_team_goal > M.home_team_goal GROUP BY M.away_team_api_id ORDER BY COUNT(*) DESC LIMIT 1
SELECT buildUpPlaySpeed FROM Team_Attributes ORDER BY buildUpPlaySpeed DESC LIMIT 4
SELECT L.name FROM ( SELECT M.league_id, COUNT(CASE WHEN M.home_team_goal = M.away_team_goal THEN 1 END) AS draw_count FROM Match M WHERE M.season = '2015/2016' GROUP BY M.league_id ) AS SubQuery JOIN League L ON SubQuery.league_id = L.id ORDER BY SubQuery.draw_count DESC LIMIT 1
SELECT CAST((strftime('%Y', 'now') - strftime('%Y', T1.birthday)) AS Integer) - (strftime('%m', 'now') < strftime('%m', T1.birthday) OR (strftime('%m', 'now') = strftime('%m', T1.birthday) AND strftime('%d', 'now') < strftime('%d', T1.birthday))) AS age FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.sprint_speed >= 97 AND strftime('%Y', T2.date) BETWEEN '2013' AND '2015'
SELECT L.name AS league_name, COUNT(M.id) AS match_count FROM `Match` M JOIN League L ON M.league_id = L.id GROUP BY L.id ORDER BY match_count DESC LIMIT 1
SELECT AVG(height) FROM Player WHERE birthday >= '1990-01-01 00:00:00' AND birthday < '1996-01-01 00:00:00'
SELECT player_api_id FROM Player_Attributes WHERE SUBSTR(date, 1, 4) = '2010' AND overall_rating = ( SELECT MAX(overall_rating) FROM Player_Attributes WHERE SUBSTR(date, 1, 4) = '2010' AND overall_rating > ( SELECT AVG(overall_rating) FROM Player_Attributes WHERE SUBSTR(date, 1, 4) = '2010' ) )
SELECT team_fifa_api_id FROM Team_Attributes WHERE buildUpPlaySpeed > 50 AND buildUpPlaySpeed < 60
SELECT T1.team_long_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlayPassing > ( SELECT AVG(buildUpPlayPassing) FROM Team_Attributes WHERE strftime('%Y', date) = '2012' ) AND strftime('%Y', T2.date) = '2012'
SELECT CAST(SUM(CASE WHEN T2.preferred_foot = 'left' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE STRFTIME('%Y', T1.birthday) BETWEEN '1987' AND '1992'
SELECT T2.name, SUM(T1.home_team_goal + T1.away_team_goal) AS total_goals FROM Match AS T1 JOIN League AS T2 ON T1.league_id = T2.id GROUP BY T2.name ORDER BY total_goals ASC LIMIT 5
SELECT CAST(SUM(T2.long_shots) AS REAL) / COUNT(T2.player_fifa_api_id) AS average_long_shots FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Ahmed Samir Farag'
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.height > 180 GROUP BY T1.player_api_id ORDER BY AVG(T2.heading_accuracy) DESC LIMIT 10
SELECT T.team_long_name FROM ( SELECT ta.team_api_id, ta.chanceCreationPassing, AVG(ta.chanceCreationPassing) OVER () AS avg_chance_creation_passing FROM Team_Attributes ta WHERE ta.buildUpPlayDribblingClass = 'Normal' AND ta.`date` >= '2014-01-01 00:00:00' AND ta.`date` <= '2014-12-31 23:59:59' ) AS subquery JOIN Team T ON subquery.team_api_id = T.team_api_id WHERE subquery.chanceCreationPassing < subquery.avg_chance_creation_passing ORDER BY subquery.chanceCreationPassing DESC
SELECT T1.name FROM League AS T1 JOIN Match AS T2 ON T1.id = T2.league_id WHERE T2.season = '2009/2010' GROUP BY T1.name HAVING CAST(SUM(T2.home_team_goal) AS REAL) / COUNT(T2.id) > CAST(SUM(T2.away_team_goal) AS REAL) / COUNT(T2.id)
SELECT team_short_name FROM Team WHERE team_long_name = 'Queens Park Rangers'
SELECT player_name FROM Player WHERE SUBSTR(birthday, 1, 4) = '1970' AND SUBSTR(birthday, 6, 2) = '10'
SELECT DISTINCT T2.attacking_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Franco Zennaro'
SELECT T2.buildUpPlayPositioningClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'ADO Den Haag'
SELECT T2.heading_accuracy FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Francois Affolter' AND T2.`date` = '2014-09-18 00:00:00'
SELECT pa.overall_rating FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Gabriel Tamas' AND strftime('%Y', pa.date) = '2011'
SELECT COUNT(*) FROM Match m JOIN League l ON m.league_id = l.id WHERE l.name = 'Scotland Premier League' AND m.season = '2015/2016'
SELECT T2.preferred_foot FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.birthday DESC LIMIT 1
SELECT P.player_name FROM Player P JOIN Player_Attributes PA ON P.player_api_id = PA.player_api_id WHERE PA.potential = (SELECT MAX(potential) FROM Player_Attributes)
SELECT COUNT(*) FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.weight < 130 AND pa.preferred_foot = 'left'
SELECT t.team_short_name FROM Team t JOIN Team_Attributes ta ON t.team_api_id = ta.team_api_id WHERE ta.chanceCreationPassingClass = 'Risky'
SELECT T2.defensive_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'David Wilson'
SELECT T1.birthday FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.overall_rating DESC LIMIT 1
SELECT T2.name FROM Country AS T1 INNER JOIN League AS T2 ON T1.id = T2.country_id WHERE T1.name = 'Netherlands'
SELECT AVG(home_team_goal) FROM Match AS T1 INNER JOIN League AS L ON T1.league_id = L.id INNER JOIN Country AS T3 ON L.country_id = T3.id WHERE T1.season = '2010/2011' AND T3.name = 'Poland'
SELECT CASE WHEN AVG(CASE WHEN p.height = (SELECT MAX(height) FROM Player) THEN pa.finishing END) > AVG(CASE WHEN p.height = (SELECT MIN(height) FROM Player) THEN pa.finishing END) THEN (SELECT player_name FROM Player WHERE height = (SELECT MAX(height) FROM Player)) ELSE (SELECT player_name FROM Player WHERE height = (SELECT MIN(height) FROM Player)) END AS PlayerWithHighestAverageFinishingRate FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id
SELECT player_name FROM Player WHERE height > 180
SELECT COUNT(*) FROM Player WHERE strftime('%Y', birthday) > '1990'
SELECT COUNT(*) FROM Player WHERE player_name LIKE 'Adam%' AND weight > 170
SELECT DISTINCT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.overall_rating > 80 AND strftime('%Y', T2.date) BETWEEN '2008' AND '2010'
SELECT pa.potential FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Aaron Doran'
SELECT P.player_name FROM Player P JOIN Player_Attributes PA ON P.player_api_id = PA.player_api_id WHERE PA.preferred_foot = 'left'
SELECT T1.team_long_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlaySpeedClass = 'Fast'
SELECT DISTINCT T2.buildUpPlayPassingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_short_name = 'CLB'
SELECT T1.team_short_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlayPassing > 70
SELECT AVG(t2.overall_rating) FROM Player AS t1 JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.height > 170 AND strftime('%Y', t2.date) BETWEEN '2010' AND '2015'
SELECT player_name FROM Player WHERE height = (SELECT MIN(height) FROM Player)
SELECT C.name FROM Country C JOIN League L ON C.id = L.country_id WHERE L.name = 'Italy Serie A'
SELECT T1.team_short_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlaySpeed = 31 AND T2.buildUpPlayDribbling = 53 AND T2.buildUpPlayPassing = 32
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Aaron Doran'
SELECT COUNT(*) FROM Match JOIN League ON Match.league_id = League.id WHERE League.name = 'Germany 1. Bundesliga' AND strftime('%Y-%m', Match.date) BETWEEN '2008-08' AND '2008-10'
SELECT T2.team_short_name FROM Match AS T1 INNER JOIN Team AS T2 ON T1.home_team_api_id = T2.team_api_id WHERE T1.home_team_goal = 10
SELECT player_api_id FROM Player_Attributes WHERE potential = 61 AND balance = ( SELECT MAX(balance) FROM Player_Attributes WHERE potential = 61 )
SELECT (SUM(CASE WHEN T1.player_name = 'Abdou Diallo' THEN T2.ball_control ELSE 0 END) / COUNT(CASE WHEN T1.player_name = 'Abdou Diallo' THEN T1.id ELSE NULL END)) - (SUM(CASE WHEN T1.player_name = 'Aaron Appindangoye' THEN T2.ball_control ELSE 0 END) / COUNT(CASE WHEN T1.player_name = 'Aaron Appindangoye' THEN T1.id ELSE NULL END)) AS difference_of_average_ball_control FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id
SELECT team_long_name FROM Team WHERE team_short_name = 'GEN'
SELECT player_name FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday ASC LIMIT 1
SELECT player_name FROM Player WHERE height = (SELECT MAX(height) FROM Player)
SELECT COUNT(*) FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
SELECT T1.name FROM Country AS T1 INNER JOIN League AS T2 ON T1.id = T2.country_id WHERE T2.name = 'Belgium Jupiler League' LIMIT 1
SELECT T2.name FROM Country AS T1 INNER JOIN League AS T2 ON T1.id = T2.country_id WHERE T1.name = 'Germany'
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
SELECT COUNT(DISTINCT T1.player_api_id) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE strftime('%Y', T1.birthday) < '1986' AND T2.defensive_work_rate = 'high'
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name IN ('Alexis', 'Ariel Borysiuk', 'Arouna Kone') ORDER BY pa.crossing DESC LIMIT 1
SELECT T2.heading_accuracy FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Ariel Borysiuk'
SELECT COUNT(*) FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.height > 180 AND pa.volleys > 70
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.volleys > 70 AND T2.dribbling > 70
SELECT COUNT(*) FROM Match m JOIN League l ON m.league_id = l.id JOIN Country c ON l.country_id = c.id WHERE m.season = '2008/2009' AND c.name = 'Belgium'
SELECT pa.long_passing FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id ORDER BY p.birthday ASC LIMIT 1
SELECT COUNT(m.id)  FROM `Match` m  JOIN League l ON m.league_id = l.id  JOIN Country c ON l.country_id = c.id  WHERE l.name = 'Belgium Jupiler League' AND SUBSTR(m.`date`, 1, 7) = '2009-04'
SELECT L.name AS league_name FROM Match M JOIN League L ON M.league_id = L.id WHERE M.season = '2008/2009' GROUP BY L.name ORDER BY COUNT(M.id) DESC LIMIT 1
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE STRFTIME('%Y', T1.birthday) < '1986'
SELECT ( (SUM(CASE WHEN T1.player_name = 'Ariel Borysiuk' THEN T2.overall_rating END) - SUM(CASE WHEN T1.player_name = 'Paulin Puel' THEN T2.overall_rating END)) / SUM(CASE WHEN T1.player_name = 'Paulin Puel' THEN T2.overall_rating END) ) * 100 AS percentage_increase FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name IN ('Ariel Borysiuk', 'Paulin Puel')
SELECT AVG(buildUpPlaySpeed) FROM Team_Attributes JOIN Team ON Team_Attributes.team_api_id = Team.team_api_id WHERE Team.team_long_name = 'Heart of Midlothian'
SELECT AVG(T1.overall_rating) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Pietro Marino'
SELECT SUM(T1.crossing) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Aaron Lennox' GROUP BY T2.player_api_id
SELECT MAX(ta.chanceCreationPassing) AS max_chance_creation_passing, ta.chanceCreationPassingClass FROM Team_Attributes ta JOIN Team t ON ta.team_api_id = t.team_api_id WHERE t.team_long_name = 'Ajax' GROUP BY ta.chanceCreationPassingClass ORDER BY max_chance_creation_passing DESC LIMIT 1
SELECT T2.preferred_foot FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Abdou Diallo'
SELECT MAX(T1.overall_rating) FROM Player_Attributes AS T1 JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Dorlan Pabon'
SELECT AVG(m.away_team_goal) AS average_goals FROM Match m JOIN Team t ON m.away_team_api_id = t.team_api_id WHERE t.team_long_name = 'Parma' AND m.country_id = (SELECT id FROM Country WHERE name = 'Italy')
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.overall_rating = 77 AND pa.date LIKE '2016-06-23%' ORDER BY p.birthday ASC LIMIT 1
SELECT T1.overall_rating FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Aaron Mooy' AND T1.date LIKE '2016-02-04%'
SELECT pa.potential FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Francesco Parravicini' AND pa.`date` = '2010-08-30 00:00:00'
SELECT T2.attacking_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Francesco Migliore' AND T2.date LIKE '2015-05-01%'
SELECT T2.defensive_work_rate FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Kevin Berigaud' AND T2.`date` = '2013-02-22 00:00:00'
SELECT MIN(`date`) FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Kevin Constant' AND pa.crossing = (SELECT MAX(crossing) FROM Player p2 JOIN Player_Attributes pa2 ON p2.player_api_id = pa2.player_api_id WHERE p2.player_name = 'Kevin Constant')
SELECT T2.buildUpPlaySpeedClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id AND T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T1.team_long_name = 'Willem II' AND T2.date = '2012-02-22'
SELECT T1.buildUpPlayDribblingClass FROM Team_Attributes AS T1 JOIN Team AS T2 ON T1.team_api_id = T2.team_api_id AND T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T2.team_short_name = 'LEI' AND T1.date = '2015-09-10 00:00:00'
SELECT T2.buildUpPlayPassingClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'FC Lorient' AND T2.date LIKE '2010-02-22%'
SELECT T2.chanceCreationPassingClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'PEC Zwolle' AND T2.date = '2013-09-20 00:00:00'
SELECT T2.chanceCreationCrossingClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Hull City' AND T2.date = '2010-02-22 00:00:00'
SELECT T2.defenceAggressionClass FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T1.team_long_name = 'Hannover 96' AND T2.date LIKE '2015-09-10%'
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T1.player_name = 'Marko Arnautovic' AND SUBSTR(T2.date, 1, 10) BETWEEN '2007-02-22' AND '2016-04-21'
SELECT    ROUND(     (       (SELECT overall_rating FROM Player_Attributes pa JOIN Player p ON pa.player_api_id = p.player_api_id WHERE p.player_name = 'Landon Donovan' AND pa.date = '2013-07-12 00:00:00') -        (SELECT overall_rating FROM Player_Attributes pa JOIN Player p ON pa.player_api_id = p.player_api_id WHERE p.player_name = 'Jordan Bowery' AND pa.date = '2013-07-12 00:00:00')     ) /      (SELECT overall_rating FROM Player_Attributes pa JOIN Player p ON pa.player_api_id = p.player_api_id WHERE p.player_name = 'Landon Donovan' AND pa.date = '2013-07-12 00:00:00')  * 100, 2) AS percentage_difference FROM Player t1 JOIN Player_Attributes t2 ON t1.player_api_id = t2.player_api_id WHERE t2.date = '2013-07-12'
SELECT player_name FROM Player ORDER BY height DESC LIMIT 1
SELECT player_api_id FROM Player ORDER BY weight DESC LIMIT 10
SELECT player_name FROM Player WHERE datetime(CURRENT_TIMESTAMP, 'localtime') - birthday > 34
SELECT SUM(home_team_goal) AS total_home_team_goals FROM Match m JOIN Player p ON m.home_player_1 = p.player_api_id OR m.home_player_2 = p.player_api_id OR m.home_player_3 = p.player_api_id OR m.home_player_4 = p.player_api_id OR m.home_player_5 = p.player_api_id OR m.home_player_6 = p.player_api_id OR m.home_player_7 = p.player_api_id OR m.home_player_8 = p.player_api_id OR m.home_player_9 = p.player_api_id OR m.home_player_10 = p.player_api_id OR m.home_player_11 = p.player_api_id WHERE p.player_name = 'Aaron Lennon'
SELECT SUM(T2.away_team_goal) FROM Player AS T1 INNER JOIN Match AS T2 ON T1.player_api_id = T2.away_player_1 OR T1.player_api_id = T2.away_player_2 OR T1.player_api_id = T2.away_player_3 OR T1.player_api_id = T2.away_player_4 OR T1.player_api_id = T2.away_player_5 OR T1.player_api_id = T2.away_player_6 OR T1.player_api_id = T2.away_player_7 OR T1.player_api_id = T2.away_player_8 OR T1.player_api_id = T2.away_player_9 OR T1.player_api_id = T2.away_player_10 OR T1.player_api_id = T2.away_player_1
SELECT SUM(T2.home_team_goal) FROM Player AS T1 INNER JOIN Match AS T2 ON T1.player_api_id = T2.home_player_1 OR T1.player_api_id = T2.home_player_2 OR T1.player_api_id = T2.home_player_3 OR T1.player_api_id = T2.home_player_4 OR T1.player_api_id = T2.home_player_5 OR T1.player_api_id = T2.home_player_6 OR T1.player_api_id = T2.home_player_7 OR T1.player_api_id = T2.home_player_8 OR T1.player_api_id = T2.home_player_9 OR T1.player_api_id = T2.home_player_10 OR T1.player_api_id = T2.home_player_1
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id AND T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T2.overall_rating = ( SELECT MAX(overall_rating) FROM Player_Attributes )
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.potential DESC LIMIT 1
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.attacking_work_rate = 'high'
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.finishing = 1 AND strftime('%Y', pa.date) - strftime('%Y', p.birthday) = ( SELECT MAX(strftime('%Y', pa2.date) - strftime('%Y', p2.birthday)) FROM Player p2 JOIN Player_Attributes pa2 ON p2.player_api_id = pa2.player_api_id WHERE pa2.finishing = 1 )
SELECT DISTINCT p.player_name FROM Player p JOIN Match m ON p.player_api_id = m.home_player_1 OR p.player_api_id = m.home_player_2 OR p.player_api_id = m.home_player_3 OR p.player_api_id = m.home_player_4 OR p.player_api_id = m.home_player_5 OR p.player_api_id = m.home_player_6 OR p.player_api_id = m.home_player_7 OR p.player_api_id = m.home_player_8 OR p.player_api_id = m.home_player_9 OR p.player_api_id = m.home_player_10 OR p.player_api_id = m.home_player_11 OR p.player_api_id = m.away_player_1 OR p.player_api_id = m.away_player_2 OR p.player_api_id = m.away_player_3 OR p.player_api_id = m.away_player_4 OR p.player_api_id = m.away_player_5 OR p.player_api_id = m.away_player_6 OR p.player_api_id = m.away_player_7 OR p.player_api_id = m.away_player_8 OR p.player_api_id = m.away_player_9 OR p.player_api_id = m.away_player_10 OR p.player_api_id = m.away_player_11
SELECT DISTINCT C.name FROM Player P JOIN Player_Attributes PA ON P.player_api_id = PA.player_api_id JOIN Match M ON P.player_api_id IN (M.home_player_1, M.home_player_2, M.home_player_3, M.home_player_4, M.home_player_5, M.home_player_6, M.home_player_7, M.home_player_8, M.home_player_9, M.home_player_10, M.home_player_11, M.away_player_1, M.away_player_2, M.away_player_3, M.away_player_4, M.away_player_5, M.away_player_6, M.away_player_7, M.away_player_8, M.away_player_9, M.away_player_10, M.away_player_11) JOIN League L ON M.league_id = L.id JOIN Country C ON L.country_id = C.id WHERE PA.vision > 89
SELECT c.name AS country_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id JOIN Country c ON p.player_fifa_api_id = c.id GROUP BY c.name ORDER BY AVG(p.weight) DESC LIMIT 1
SELECT T1.team_long_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.buildUpPlaySpeedClass = 'Slow'
SELECT T1.team_short_name FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_api_id = T2.team_api_id WHERE T2.chanceCreationPassingClass = 'Safe'
SELECT AVG(T5.height) FROM Country AS T1 INNER JOIN League AS T2 ON T1.id = T2.country_id INNER JOIN Match AS T3 ON T2.id = T3.league_id INNER JOIN Player AS T5 ON T3.home_player_1 = T5.player_api_id OR T3.home_player_2 = T5.player_api_id OR T3.home_player_3 = T5.player_api_id OR T3.home_player_4 = T5.player_api_id OR T3.home_player_5 = T5.player_api_id OR T3.home_player_6 = T5.player_api_id OR T3.home_player_7 = T5.player_api_id OR T3.home_player_8 = T5.player_api_id OR T3.home_player_9 = T5.player_api_id
SELECT player_name FROM Player WHERE height > 180 ORDER BY player_name ASC LIMIT 3
SELECT COUNT(*) FROM Player WHERE player_name LIKE 'Aaron%' AND birthday > '1990'
SELECT (SELECT jumping FROM Player_Attributes WHERE id = 6) - (SELECT jumping FROM Player_Attributes WHERE id = 23) AS difference
SELECT pa.player_api_id FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.preferred_foot = 'right' ORDER BY pa.potential ASC LIMIT 5
SELECT COUNT(*) FROM Player_Attributes WHERE preferred_foot = 'left' AND crossing = (SELECT MAX(crossing) FROM Player_Attributes)
SELECT CAST(COUNT(CASE WHEN strength > 80 AND stamina > 80 THEN 1 END) AS REAL) * 100 / COUNT(*) FROM Player_Attributes
SELECT T2.name FROM League AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T1.name = 'Poland Ekstraklasa'
SELECT T1.home_team_goal, T1.away_team_goal FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T2.name = 'Belgium Jupiler League' AND T1.date LIKE '2008-09-24%'
SELECT pa.sprint_speed, pa.agility, pa.acceleration FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Alexis Blin'
SELECT T2.buildUpPlaySpeedClass FROM Team AS T1 JOIN Team_Attributes AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T1.team_long_name = 'KSV Cercle Brugge'
SELECT COUNT(*) FROM Match m JOIN League l ON m.league_id = l.id WHERE l.name = 'Italy Serie A' AND m.season = '2015/2016'
SELECT DISTINCT MAX(home_team_goal) FROM Match AS T1 INNER JOIN League AS T2 ON T1.league_id = T2.id WHERE T2.name = 'Netherlands Eredivisie'
SELECT pa.finishing, pa.curve FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id ORDER BY p.weight DESC LIMIT 1
SELECT L.name  FROM Match M  JOIN League L ON M.league_id = L.id  WHERE M.season = '2015/2016'  GROUP BY L.name  ORDER BY COUNT(M.id) DESC  LIMIT 4
SELECT T2.team_long_name FROM Match AS T1 JOIN Team AS T2 ON T1.away_team_api_id = T2.team_api_id ORDER BY T1.away_team_goal DESC LIMIT 1
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id ORDER BY pa.overall_rating DESC LIMIT 1
SELECT CAST(COUNT(CASE WHEN p.height < 180 AND pa.overall_rating > 70 THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) AS percentage FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id
SELECT     (CASE WHEN COUNT(CASE WHEN Admission = '+' THEN 1 END) > COUNT(CASE WHEN Admission = '-' THEN 1 END) THEN 'in-patient' ELSE 'outpatient' END) AS group_with_more_males,     (ABS(COUNT(CASE WHEN Admission = '+' THEN 1 END) - COUNT(CASE WHEN Admission = '-' THEN 1 END)) / COUNT(CASE WHEN Admission = '-' THEN 1 END) * 100) AS percentage_deviation FROM Patient WHERE SEX = 'M'
SELECT CAST(COUNT(CASE WHEN STRFTIME('%Y', Birthday) > '1930' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(*) FROM Patient WHERE SEX = 'F'
SELECT CAST(SUM(CASE WHEN Admission = '+' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient WHERE STRFTIME('%Y', Birthday) BETWEEN '1930' AND '1940'
SELECT CAST(COUNT(CASE WHEN Admission = '-' THEN 1 END) AS REAL) / COUNT(CASE WHEN Admission = '+' THEN 1 END) AS outpatient_to_inpatient_ratio FROM Patient WHERE Diagnosis = 'SLE'
SELECT Diagnosis, Date FROM Patient JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Patient.ID = 30609
SELECT p.SEX, p.Birthday, e.`Examination Date`, e.Symptoms FROM Patient p JOIN Examination e ON p.ID = e.ID WHERE p.ID = '163109'
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.LDH > 500
SELECT T1.ID, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.Birthday) AS Age FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.RVVT = '+'
SELECT T1.ID, T1.SEX, T1.Diagnosis FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.Thrombosis = 2
SELECT T1.ID FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T2.Birthday) = '1937' AND T1.`T-CHO` >= 250
SELECT T1.ID, T1.SEX, T1.Diagnosis FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.ALB < 3.5
SELECT CAST(COUNT(CASE WHEN T2.TP < 6.0 OR T2.TP > 8.5 THEN 1 END) AS REAL) * 100 / COUNT(T1.ID) AS percentage_female_with_tp_out_of_range FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F'
SELECT AVG(T1.`aCL IgG`) FROM Examination AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.Admission = '+' AND strftime('%Y', 'now') - strftime('%Y', T2.Birthday) >= 50
SELECT COUNT(*) FROM Patient WHERE SEX = 'F' AND Admission = '-' AND STRFTIME('%Y', Description) = '1997'
SELECT MIN(STRFTIME('%Y', `First Date`) - STRFTIME('%Y', Birthday)) AS min_age FROM Patient
SELECT COUNT(DISTINCT p.ID) FROM Examination e JOIN Patient p ON e.ID = p.ID WHERE e.Thrombosis = '1' AND p.sex = 'F' AND STRFTIME('%Y', e.`Examination Date`) = '1997'
SELECT MAX(STRFTIME('%Y', T1.Birthday)) - MIN(STRFTIME('%Y', T1.Birthday)) AS AgeGap FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TG >= 200
SELECT T1.Symptoms, T1.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.Symptoms IS NOT NULL ORDER BY T2.Birthday DESC LIMIT 1
SELECT CAST(COUNT(*) AS REAL) / 12 FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.Date >= '1998-01-01' AND l.Date < '1999-01-01'
SELECT T2.`Date`, strftime('%Y', T1.`First Date`) - strftime('%Y', T1.Birthday) AS Age FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SJS' ORDER BY T1.Birthday ASC LIMIT 1
SELECT CAST(SUM(IIF(T1.SEX = 'M', 1, 0)) AS REAL) / SUM(IIF(T1.SEX = 'F', 1, 0)) AS male_to_female_ratio FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T1.SEX = 'M' AND T2.UA <= 8.0) OR (T1.SEX = 'F' AND T2.UA <= 6.5)
SELECT COUNT(DISTINCT p.ID) AS NumberOfPatients FROM Patient p JOIN Examination e ON p.ID = e.ID WHERE STRFTIME('%Y', e.`Examination Date`) - STRFTIME('%Y', p.`First Date`) >= 1
SELECT COUNT(DISTINCT p.ID) AS underage_patients_count FROM Examination e JOIN Patient p ON e.ID = p.ID WHERE e.`Examination Date` BETWEEN '1990-01-01' AND '1993-12-31'   AND STRFTIME('%Y', e.`Examination Date`) - STRFTIME('%Y', p.Birthday) < 18
SELECT COUNT(T2.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.`T-BIL` >= 2.0
SELECT Diagnosis FROM Examination WHERE `Examination Date` BETWEEN '1985-01-01' AND '1995-12-31' GROUP BY Diagnosis ORDER BY COUNT(Diagnosis) DESC LIMIT 1
SELECT AVG(1999 - strftime('%Y', T1.Birthday)) AS average_age FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.Date BETWEEN '1991-10-01' AND '1991-10-31'
SELECT (strftime('%Y', T1.`Examination Date`) - strftime('%Y', T3.Birthday)) AS Age, T1.Diagnosis FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID INNER JOIN Patient AS T3 ON T2.ID = T3.ID ORDER BY T2.HGB DESC LIMIT 1
SELECT ANA FROM Examination WHERE ID = 3605340 AND `Examination Date` = '1996-12-02'
SELECT CASE WHEN "T-CHO" < 250 THEN 1 ELSE 0 END AS status FROM Laboratory WHERE ID = 2927464 AND Date = '1995-09-04'
SELECT SEX FROM Patient WHERE Diagnosis = 'AORTITIS' ORDER BY Description ASC LIMIT 1
SELECT T2.`aCL IgM` FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T1.Description = '1994-02-19' AND T2.`Examination Date` = '1993-11-12'
SELECT T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GPT = 9 AND T2.Date = '1992-06-12'
SELECT STRFTIME('%Y', T2.`Date`) - STRFTIME('%Y', T1.Birthday) AS age FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.Date = '1991-10-21' AND T2.UA = '8.4'
SELECT COUNT(ID) FROM Laboratory WHERE ID IN (SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS') AND strftime('%Y', Date) = '1995'
SELECT T2.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T1.`Examination Date` = '1997-01-27'
SELECT T2.Symptoms FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.Birthday = '1959-03-01' AND T2.`Examination Date` = '1993-09-27'
SELECT      (SUM(CASE WHEN T2.Date LIKE '1981-11%' THEN T2.`T-CHO` ELSE 0 END) -       SUM(CASE WHEN T2.Date LIKE '1981-12%' THEN T2.`T-CHO` ELSE 0 END)) AS decrease_rate  FROM Patient AS T1  JOIN Laboratory AS T2 ON T1.ID = T2.ID  WHERE T1.Birthday = '1959-02-18'
SELECT P.ID FROM Patient P JOIN Examination E ON P.ID = E.ID WHERE E.Diagnosis = 'Behcet' AND E.`Examination Date` BETWEEN '1997-01-01' AND '1997-12-31'
SELECT ID FROM Laboratory WHERE `Date` BETWEEN '1987-07-06' AND '1996-01-31' AND GPT > 30 AND ALB < 4
SELECT ID FROM Patient WHERE SEX = 'F' AND STRFTIME('%Y', Birthday) = '1964' AND Admission = '+'
SELECT COUNT(*) FROM Examination WHERE Thrombosis = 2 AND `ANA Pattern` = 'S' AND `aCL IgM` >= (SELECT AVG(`aCL IgM`) * 1.2 FROM Examination WHERE Thrombosis = 2 AND `ANA Pattern` = 'S')
SELECT CAST(SUM(CASE WHEN UA <= 6.5 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS percentage FROM Laboratory WHERE `U-PRO` > 0 AND `U-PRO` < 30
SELECT CAST(SUM(CASE WHEN Diagnosis = 'BEHCET' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient WHERE SEX = 'M' AND strftime('%Y', `First Date`) = '1981'
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.Date LIKE '1991-10%' AND T2.`T-BIL` < 2.0
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND STRFTIME('%Y', T1.Birthday) BETWEEN '1980' AND '1989' AND T2.`ANA Pattern` != 'P'
SELECT DISTINCT T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID INNER JOIN Examination AS T3 ON T1.ID = T3.ID WHERE T3.Diagnosis = 'PSS' AND T2.CRP > 2 AND T2.CRE = 1 AND T2.LDH = 123
SELECT AVG(L.ALB) FROM Laboratory L JOIN Patient P ON L.ID = P.ID WHERE P.SEX = 'F' AND L.PLT > 400 AND P.Diagnosis = 'SLE'
SELECT Symptoms FROM Examination JOIN Patient ON Examination.ID = Patient.ID WHERE Patient.Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1
SELECT Description, Diagnosis FROM Patient WHERE ID = 48473
SELECT COUNT(ID) FROM Patient WHERE SEX = 'F' AND Diagnosis = 'APS'
SELECT COUNT(ID) FROM Laboratory WHERE STRFTIME('%Y', Date) = '1997' AND (TP <= 6 OR TP >= 8.5)
SELECT CAST(SUM(CASE WHEN T2.Diagnosis LIKE '%SLE%' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Examination AS T1 JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.Symptoms LIKE '%thrombocytopenia%'
SELECT CAST(SUM(CASE WHEN SEX = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient WHERE STRFTIME('%Y', Birthday) = '1980' AND Diagnosis = 'RA'
SELECT COUNT(DISTINCT p.ID)  FROM Patient p  JOIN Examination e ON p.ID = e.ID  WHERE p.SEX = 'M'  AND e.`Examination Date` BETWEEN '1995-01-01' AND '1997-12-31'  AND e.Diagnosis = 'Behcet'  AND p.Admission = '-'
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND T2.WBC < 3.5
SELECT julianday(T2.`Examination Date`) - julianday(T1.`First Date`) AS days_difference FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = 821298
SELECT CASE WHEN (SEX = 'M' AND UA > 8.0) OR (SEX = 'F' AND UA > 6.5) THEN 'Yes' ELSE 'No' END AS Is_UA_Within_Normal_Range FROM Laboratory JOIN Patient ON Laboratory.ID = Patient.ID WHERE Patient.ID = 57266
SELECT Date FROM Laboratory WHERE ID = 48473 AND GOT >= 60
SELECT T2.SEX, T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Date) = '1994' AND T1.GOT < 60
SELECT DISTINCT T2.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.GPT >= 60
SELECT T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.GPT > 60 ORDER BY T2.Birthday ASC
SELECT AVG(LDH) FROM Laboratory WHERE LDH < 500
SELECT P.ID, strftime('%Y', current_timestamp) - strftime('%Y', P.Birthday) AS age FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE L.LDH BETWEEN 600 AND 800
SELECT DISTINCT T1.Admission FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.ALP < 300
SELECT P.ID, L.ALP < 300 AS ALP_within_normal_range FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE P.Birthday = '1982-04-01'
SELECT p.ID, p.SEX, p.Birthday FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.TP < 6.0
SELECT L.TP - 8.5 AS Deviation FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE P.SEX = 'F' AND L.TP > 8.5
SELECT p.Birthday FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND (l.ALB <= 3.5 OR l.ALB >= 5.5) ORDER BY p.Birthday DESC
SELECT P.ID, CASE WHEN L.ALB BETWEEN 3.5 AND 5.5 THEN 'Yes' ELSE 'No' END AS Albumin_within_normal_range FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE STRFTIME('%Y', P.Birthday) = '1982'
SELECT (CAST(SUM(CASE WHEN L.UA > 6.5 THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100 AS Percentage FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE P.SEX = 'F'
SELECT AVG(l.UA) AS average_UA_index FROM ( SELECT ID, MAX(Date) AS latest_date FROM Laboratory GROUP BY ID ) AS latest_exams JOIN Laboratory l ON latest_exams.ID = l.ID AND latest_exams.latest_date = l.Date JOIN Patient p ON l.ID = p.ID WHERE (p.SEX = 'M' AND l.UA < 8.0) OR (p.SEX = 'F' AND l.UA < 6.5)
SELECT T1.ID, T1.SEX, T1.Birthday FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.UN = 29
SELECT T2.ID, T2.SEX, T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.Diagnosis = 'RA' AND T1.UN < 30
SELECT COUNT(*) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CRE >= 1.5 AND T1.SEX = 'M'
SELECT (SUM(CASE WHEN t1.sex = 'M' THEN 1 ELSE 0 END) > SUM(CASE WHEN t1.sex = 'F' THEN 1 ELSE 0 END)) AS result FROM patient AS t1 INNER JOIN laboratory AS t2 ON t1.id = t2.id WHERE t2.cre >= 1.5
SELECT P.ID, P.SEX, P.Birthday FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE L.`T-BIL` = (SELECT MAX(`T-BIL`) FROM Laboratory)
SELECT SEX, GROUP_CONCAT(DISTINCT T1.ID) AS ID_LIST FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`T-BIL` >= 2.0 GROUP BY T1.SEX
SELECT T1.ID, T2.`T-CHO` FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID ORDER BY T1.Birthday ASC, T2.`T-CHO` DESC LIMIT 1
SELECT AVG(strftime('%Y', 'now') - strftime('%Y', p.Birthday)) AS average_age FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.`T-CHO` >= 250
SELECT DISTINCT T1.ID, T2.Diagnosis FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TG > 300
SELECT COUNT(DISTINCT T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.TG >= 200 AND CAST(STRFTIME('%Y', CURRENT_TIMESTAMP) AS INT) - CAST(STRFTIME('%Y', T2.Birthday) AS INT) > 50
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.CPK < 250
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Birthday) BETWEEN '1936' AND '1956' AND T1.SEX = 'M' AND T2.CPK >= 250
SELECT DISTINCT T1.ID, T1.SEX, strftime('%Y', current_timestamp) - strftime('%Y', T1.Birthday) AS Age FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GLU >= 180 AND T2.`T-CHO` < 250
SELECT T1.ID, T2.GLU FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GLU < 180 AND STRFTIME('%Y', T1.Description) = '1991'
SELECT p.ID, p.SEX, p.Birthday FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.WBC <= 3.5 OR l.WBC >= 9.0 GROUP BY p.SEX ORDER BY strftime('%Y', 'now') - strftime('%Y', p.Birthday)
SELECT T1.ID, T1.Diagnosis, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.Birthday) AS Age FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RBC < 3.5
SELECT p.Admission FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'F' AND (strftime('%Y', current_timestamp) - strftime('%Y', p.Birthday)) >= 50 AND (l.RBC <= 3.5 OR l.RBC >= 6.0)
SELECT DISTINCT T1.ID, T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '-' AND T2.HGB < 10
SELECT T1.ID, T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T2.HGB > 10 AND T2.HGB < 17 ORDER BY T1.Birthday ASC LIMIT 1
SELECT P.ID, (strftime('%Y', 'now') - strftime('%Y', P.Birthday)) AS age FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE L.HCT >= 52 GROUP BY P.ID HAVING COUNT(L.ID) >= 2
SELECT AVG(HCT) FROM Laboratory WHERE Date LIKE '1991%' AND HCT < 29
SELECT SUM(IIF(PLT < 100, 1, 0)) - SUM(IIF(PLT > 400, 1, 0)) AS comparison_result FROM Laboratory WHERE PLT <= 100 OR PLT >= 400
SELECT T1.ID FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE strftime('%Y', T1.Date) = '1984' AND T1.PLT BETWEEN 100 AND 400 AND strftime('%Y', 'now') - strftime('%Y', T2.Birthday) < 50
SELECT CAST(SUM(CASE WHEN Patient.SEX = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM Patient JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE strftime('%Y', current_timestamp) - strftime('%Y', Patient.Birthday) > 55 AND Laboratory.PT >= 14
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.`First Date` > '1992-12-31' AND T2.PT < 14
SELECT COUNT(*) FROM Examination AS E JOIN Laboratory AS L ON E.ID = L.ID WHERE E.`Examination Date` > '1997-01-01' AND L.APTT < 45
SELECT COUNT(DISTINCT T2.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.APTT > 45 AND T2.Thrombosis = 0
SELECT COUNT(DISTINCT p.ID) FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.WBC > 3.5 AND l.WBC < 9.0 AND (l.FG <= 150 OR l.FG >= 450)
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Birthday > '1980-01-01' AND (T2.FG < 150 OR T2.FG > 450)
SELECT DISTINCT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`U-PRO` >= 30
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`U-PRO` > 0 AND T2.`U-PRO` < 30 AND T1.Diagnosis = 'SLE'
SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE IGG >= 2000
SELECT SUM(CASE WHEN Symptoms IS NOT NULL THEN 1 ELSE 0 END) AS PatientCount FROM Laboratory L JOIN Examination E ON L.ID = E.ID WHERE L.IGG BETWEEN 901 AND 1999
SELECT Diagnosis FROM Patient WHERE ID = (SELECT ID FROM Laboratory WHERE IGA = (SELECT MAX(IGA) FROM Laboratory WHERE IGA BETWEEN 80 AND 500))
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGA > 80 AND T2.IGA < 500 AND STRFTIME('%Y', T1.`First Date`) >= '1990'
SELECT p.Diagnosis FROM Laboratory l JOIN Patient p ON l.ID = p.ID WHERE l.IGM <= 40 OR l.IGM >= 400 GROUP BY p.Diagnosis ORDER BY COUNT(p.Diagnosis) DESC LIMIT 1
SELECT COUNT(*) FROM Laboratory l LEFT JOIN Patient p ON l.ID = p.ID WHERE l.CRP = '+' AND p.Description IS NULL
SELECT COUNT(*) FROM Laboratory L JOIN Patient P ON L.ID = P.ID WHERE L.CRE >= 1.5 AND strftime('%Y', CURRENT_DATE) - strftime('%Y', P.Birthday) < 70
SELECT COUNT(DISTINCT T1.ID) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RA = '-' AND T1.KCT = '+'
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T1.Birthday) >= '1985' AND T2.RA IN ('-', '+-')
SELECT p.ID FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.RF < 20 AND strftime('%Y', 'now') - strftime('%Y', p.Birthday) > 60
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.RF < 20 AND T2.Thrombosis = 0
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.C3 > 35 AND T2.`ANA Pattern` = 'P'
SELECT T2.ID FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.HCT < 29 OR T1.HCT > 52 ORDER BY T2.`aCL IgA` DESC LIMIT 1
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'APS' AND T2.C4 > 10
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RNP = '0' AND T1.Admission = '+'
SELECT p.Birthday FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.RNP NOT IN ('-', '+-') ORDER BY p.Birthday DESC LIMIT 1
SELECT COUNT(*) FROM Examination e JOIN Laboratory l ON e.ID = l.ID WHERE (l.SM = 'negative' OR l.SM = '0') AND e.Thrombosis = 0
SELECT T2.ID FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.SM NOT IN ('negative', '0') ORDER BY T2.Birthday DESC LIMIT 3
SELECT ID FROM Laboratory WHERE Date > '1997-01-01' AND SC170 IN ('negative', '0')
SELECT COUNT(DISTINCT p.ID)  FROM Patient p  JOIN Laboratory l ON p.ID = l.ID  JOIN Examination e ON p.ID = e.ID  WHERE l.SC170 IN ('negative', '0')  AND p.SEX = 'F'  AND e.Symptoms IS NULL
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.SSA IN ('0', '+') AND STRFTIME('%Y', T1.`First Date`) < '2000'
SELECT p.ID FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.SSA NOT IN ('negative', '0') ORDER BY p.`First Date` ASC LIMIT 1
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.SSB IN ('-', '0') AND T2.Diagnosis = 'SLE'
SELECT COUNT(DISTINCT T2.ID) FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 ON T2.ID = T3.ID WHERE T3.SSB IN ('negative', '0') AND T1.Symptoms IS NOT NULL
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Sex = 'M' AND T2.CENTROMEA IN ('0', 'negative') AND T2.SSB IN ('0', 'negative')
SELECT DISTINCT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.DNA >= 8
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Description IS NULL AND T2.DNA < 8
SELECT COUNT(T2.ID) FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.Admission = '+' AND T1.IGG > 900 AND T1.IGG < 2000
SELECT CAST(COUNT(CASE WHEN T1.GOT >= 60 AND T2.Diagnosis = 'SLE' THEN 1 END) AS REAL) * 100 / COUNT(CASE WHEN T1.GOT >= 60 THEN 1 END) AS percentage FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID
SELECT COUNT(*) FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.GOT < 60
SELECT T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GOT >= 60 ORDER BY T1.Birthday DESC LIMIT 1
SELECT DISTINCT T2.Birthday FROM Laboratory AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.GPT < 60 ORDER BY T1.GPT DESC LIMIT 3
SELECT COUNT(*) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GPT < 60 AND T1.SEX = 'M'
SELECT p.`First Date` FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE l.LDH < 500 ORDER BY l.LDH DESC LIMIT 1
SELECT MAX(`Date`) AS latest_date FROM Laboratory WHERE ID IN ( SELECT ID FROM Patient ORDER BY `First Date` DESC LIMIT 1 ) AND LDH >= 500
SELECT COUNT(*) FROM Laboratory AS L JOIN Patient AS P ON L.ID = P.ID WHERE L.ALP >= 300 AND P.Admission = '+'
SELECT COUNT(t2.ID) FROM Patient AS t1 INNER JOIN Laboratory AS t2 ON t1.ID = t2.ID WHERE t1.Admission = '-' AND t2.ALP < 300
SELECT Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TP < 6.0
SELECT COUNT(P.ID) FROM Patient P JOIN Laboratory L ON P.ID = L.ID WHERE P.Diagnosis = 'SJS' AND L.TP > 6.0 AND L.TP < 8.5
SELECT T2.`Examination Date` FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ALB > 3.5 AND T1.ALB < 5.5 ORDER BY T1.ALB DESC LIMIT 1
SELECT COUNT(*) FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.ALB > 3.5 AND l.ALB < 5.5 AND l.TP BETWEEN 6.0 AND 8.5
SELECT E.`aCL IgG`, E.`aCL IgM`, E.`aCL IgA` FROM Patient P JOIN Examination E ON P.ID = E.ID JOIN Laboratory L ON P.ID = L.ID WHERE P.SEX = 'F' AND L.UA > 6.50 ORDER BY L.UA DESC LIMIT 1
SELECT MAX(T1.ANA) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CRE < 1.5
SELECT T2.ID FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.CRE < 1.5 ORDER BY T2.`aCL IgA` DESC LIMIT 1
SELECT COUNT(*) FROM Laboratory l JOIN Examination e ON l.ID = e.ID WHERE l.`T-BIL` >= 2.0 AND e.`ANA Pattern` LIKE '%P%'
SELECT T1.ANA FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`T-BIL` < 2.0 ORDER BY T2.`T-BIL` DESC LIMIT 1
SELECT COUNT(E.ID) FROM Laboratory L JOIN Examination E ON L.ID = E.ID WHERE L.`T-CHO` >= 250 AND E.KCT = '-'
SELECT COUNT(*) FROM Laboratory AS L JOIN Examination AS E ON L.ID = E.ID WHERE L.`T-CHO` < 250 AND E.`ANA Pattern` = 'P'
SELECT COUNT(E.ID) FROM Examination E JOIN Laboratory L ON E.ID = L.ID WHERE L.TG < 200 AND E.Symptoms IS NOT NULL
SELECT T1.Diagnosis FROM Patient AS T1 JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.TG < 200 ORDER BY T2.TG DESC LIMIT 1
SELECT DISTINCT P.ID FROM Patient P JOIN Examination E ON P.ID = E.ID JOIN Laboratory L ON P.ID = L.ID WHERE E.Thrombosis = 0 AND L.CPK < 250
SELECT COUNT(T1.ID) FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.CPK < 250 AND (T1.KCT = '+' OR T1.RVVT = '+' OR T1.LAC = '+')
SELECT T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GLU > 180 ORDER BY T1.Birthday ASC LIMIT 1
SELECT COUNT(*) FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.GLU < 180 AND T2.Thrombosis = 0
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Admission = '+' AND T2.WBC BETWEEN 3.5 AND 9.0
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T2.WBC BETWEEN 3.5 AND 9.0
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T2.RBC <= 3.5 OR T2.RBC >= 6.0) AND T1.Admission = '-'
SELECT COUNT(*) FROM Patient AS p INNER JOIN Laboratory AS l ON p.ID = l.ID WHERE l.PLT > 100 AND l.PLT < 400 AND p.Diagnosis IS NOT NULL
SELECT L.PLT FROM Laboratory L INNER JOIN Patient P ON L.ID = P.ID WHERE P.Diagnosis = 'MCTD' AND L.PLT > 100 AND L.PLT < 400
SELECT AVG(L.PT) AS average_prothrombin_time FROM Laboratory L JOIN Patient P ON L.ID = P.ID WHERE P.SEX = 'M' AND L.PT < 14
SELECT COUNT(DISTINCT p.ID) AS NumberOfPatients FROM Patient p JOIN Examination e ON p.ID = e.ID JOIN Laboratory l ON p.ID = l.ID WHERE e.Thrombosis IN (1, 2) AND l.PT < 14
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Angela' AND T1.last_name = 'Sanders'
SELECT COUNT(*) FROM member JOIN major ON member.link_to_major = major.major_id WHERE major.college = 'College of Engineering'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.department = 'Art and Design Department'
SELECT COUNT(DISTINCT link_to_member) AS number_of_students FROM attendance WHERE link_to_event = (SELECT event_id FROM event WHERE event_name = 'Women''s Soccer')
SELECT T3.phone FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.event_name = 'Women''s Soccer'
SELECT COUNT(*) FROM event e JOIN attendance a ON e.event_id = a.link_to_event JOIN member m ON a.link_to_member = m.member_id WHERE e.event_name = 'Women''s Soccer' AND m.t_shirt_size = 'Medium'
SELECT e.event_name FROM event e JOIN attendance a ON e.event_id = a.link_to_event GROUP BY e.event_id ORDER BY COUNT(a.link_to_member) DESC LIMIT 1
SELECT m.college FROM major m JOIN member me ON m.major_id = me.link_to_major WHERE me.position = 'Vice President'
SELECT T1.event_name FROM event AS T1 JOIN attendance AS T2 ON T1.event_id = T2.link_to_event JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T3.first_name = 'Maya' AND T3.last_name = 'Mclean'
SELECT COUNT(*) FROM attendance AS T2 JOIN member AS T1 ON T1.member_id = T2.link_to_member JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T1.first_name = 'Sacha' AND T1.last_name = 'Harrison' AND STRFTIME('%Y', T3.event_date) = '2019'
SELECT COUNT(*) FROM ( SELECT e.event_id FROM event e JOIN attendance a ON e.event_id = a.link_to_event WHERE e.type = 'Meeting' GROUP BY e.event_id HAVING COUNT(a.link_to_member) > 10 ) AS meetings_with_more_than_10_attendees
SELECT e.event_name FROM event e JOIN attendance a ON e.event_id = a.link_to_event LEFT JOIN budget b ON e.event_id = b.link_to_event GROUP BY e.event_id HAVING COUNT(a.link_to_member) > 20 AND (b.category NOT IN ('Food', 'Advertisement') OR b.amount <= 150)
SELECT CAST(COUNT(e.event_id) AS REAL) / COUNT(DISTINCT e.event_name) AS average_attendance FROM event e JOIN attendance a ON e.event_id = a.link_to_event WHERE e.type = 'Meeting' AND STRFTIME('%Y', e.event_date) = '2020'
SELECT expense_description FROM expense ORDER BY cost DESC LIMIT 1
SELECT COUNT(m.member_id) FROM member m JOIN major ma ON m.link_to_major = ma.major_id WHERE ma.major_name = 'Environmental Engineering'
SELECT m.first_name, m.last_name FROM event e JOIN attendance a ON e.event_id = a.link_to_event JOIN member m ON a.link_to_member = m.member_id WHERE e.event_name = 'Laugh Out Loud'
SELECT T2.last_name FROM major AS T1 JOIN member AS T2 ON T1.major_id = T2.link_to_major WHERE T1.major_name = 'Law and Constitutional Studies'
SELECT T2.county FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Sherri' AND T1.last_name = 'Ramsey'
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Tyler' AND T1.last_name = 'Hewitt'
SELECT SUM(T2.amount) FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.position = 'Vice President'
SELECT SUM(b.spent) AS total_spent_on_food FROM budget b JOIN event e ON b.link_to_event = e.event_id WHERE b.category = 'Food' AND e.event_name = 'September Meeting'
SELECT z.city, z.state FROM member m JOIN zip_code z ON m.zip = z.zip_code WHERE m.position = 'President'
SELECT member.first_name, member.last_name FROM member JOIN zip_code ON member.zip = zip_code.zip_code WHERE zip_code.state = 'Illinois'
SELECT b.spent FROM budget b JOIN event e ON b.link_to_event = e.event_id WHERE e.event_name = 'September Meeting' AND b.category = 'Advertisement'
SELECT DISTINCT m.department FROM major m JOIN member me ON me.link_to_major = m.major_id WHERE me.last_name IN ('Pierce', 'Guidi')
SELECT SUM(amount) FROM event JOIN budget ON event.event_id = budget.link_to_event WHERE event.event_name = 'October Speaker'
SELECT approved FROM expense WHERE approved = 'true' AND link_to_budget IN (SELECT budget_id FROM budget WHERE link_to_event = (SELECT event_id FROM event WHERE event_name = 'October Meeting' AND event_date LIKE '2019-10-08%'))
SELECT SUM(e.cost) / COUNT(e.expense_id) AS average_cost FROM member m JOIN expense e ON m.member_id = e.link_to_member WHERE m.member_id = (SELECT member_id FROM member WHERE first_name = 'Elijah' AND last_name = 'Allen') AND (SUBSTR(e.expense_date, 6, 2) = '09' OR SUBSTR(e.expense_date, 6, 2) = '10')
SELECT SUM(CASE WHEN STRFTIME('%Y', T2.event_date) = '2019' THEN T1.spent ELSE 0 END) - SUM(CASE WHEN STRFTIME('%Y', T2.event_date) = '2020' THEN T1.spent ELSE 0 END) AS difference FROM budget AS T1 JOIN event AS T2 ON T1.link_to_event = T2.event_id
SELECT location FROM event WHERE event_name = 'Spring Budget Review'
SELECT cost FROM expense WHERE expense_description = 'Posters' AND expense_date = '2019-09-04'
SELECT remaining FROM budget WHERE category = 'Food' AND amount = (SELECT MAX(amount) FROM budget WHERE category = 'Food')
SELECT notes FROM income WHERE source = 'Fundraising' AND date_received = '2019-09-14'
SELECT COUNT(major_name) FROM major WHERE college = 'College of Humanities and Social Sciences'
SELECT phone FROM member WHERE first_name = 'Carlo' AND last_name = 'Jacobs'
SELECT T2.county FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Adela' AND T1.last_name = 'O''Gallagher'
SELECT COUNT(*) FROM budget AS b JOIN event AS e ON b.link_to_event = e.event_id WHERE e.event_name = 'November Meeting' AND b.remaining < 0
SELECT SUM(b.amount) FROM event e JOIN budget b ON e.event_id = b.link_to_event WHERE e.event_name = 'September Speaker'
SELECT T2.event_status FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id WHERE T1.expense_description = 'Post Cards, Posters' AND T1.expense_date = '2019-08-20'
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Brent' AND T1.last_name = 'Thomason'
SELECT COUNT(*) FROM member JOIN major ON member.link_to_major = major.major_id WHERE major.major_name = 'Business' AND member.t_shirt_size = 'Medium'
SELECT T2.type FROM member AS T1 JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Christof' AND T1.last_name = 'Nielson'
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'Vice President'
SELECT T2.state FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Sacha' AND T1.last_name = 'Harrison'
SELECT DISTINCT T2.department FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'President'
SELECT t2.date_received FROM member AS t1 INNER JOIN income AS t2 ON t1.member_id = t2.link_to_member WHERE t1.first_name = 'Connor' AND t1.last_name = 'Hilton' AND t2.source = 'Dues'
SELECT m.first_name, m.last_name FROM member m JOIN income i ON m.member_id = i.link_to_member WHERE i.source = 'Dues' ORDER BY i.date_received ASC LIMIT 1
SELECT SUM(CASE WHEN T2.event_name = 'Yearly Kickoff' THEN T1.amount ELSE 0 END) / SUM(CASE WHEN T2.event_name = 'October Meeting' THEN T1.amount ELSE 0 END) AS budget_ratio FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.category = 'Advertisement'
SELECT CAST(SUM(IIF(T2.category = 'Parking', T2.amount, 0)) AS REAL) * 100 / SUM(T2.amount) AS parking_percentage FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'November Speaker'
SELECT SUM(cost) FROM expense WHERE expense_description = 'Pizza'
SELECT COUNT(city) FROM zip_code WHERE county = 'Orange County' AND state = 'Virginia'
SELECT department FROM major WHERE college = 'College of Humanities and Social Sciences'
SELECT T1.city, T1.county, T1.state FROM zip_code AS T1 INNER JOIN member AS T2 ON T1.zip_code = T2.zip WHERE T2.first_name = 'Amy' AND T2.last_name = 'Firth'
SELECT T1.expense_description FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id WHERE T2.remaining = ( SELECT MIN(remaining) FROM budget )
SELECT m.first_name, m.last_name FROM member m JOIN attendance a ON m.member_id = a.link_to_member JOIN event e ON a.link_to_event = e.event_id WHERE e.event_name = 'October Meeting'
SELECT major.college FROM member JOIN major ON member.link_to_major = major.major_id GROUP BY major.college ORDER BY COUNT(member.member_id) DESC LIMIT 1
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.phone = '809-555-3360'
SELECT E.event_name FROM event AS E JOIN budget AS B ON E.event_id = B.link_to_event ORDER BY B.amount DESC LIMIT 1
SELECT T1.expense_description FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T2.position = 'Vice President'
SELECT COUNT(T2.link_to_member) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'Women''s Soccer'
SELECT T2.date_received FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.first_name = 'Casey' AND T1.last_name = 'Mason'
SELECT COUNT(*) FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.state = 'Maryland'
SELECT COUNT(DISTINCT e.event_id) AS number_of_events_attended FROM member m JOIN attendance a ON m.member_id = a.link_to_member JOIN event e ON a.link_to_event = e.event_id WHERE m.phone = '954-555-6240'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.department = "School of Applied Sciences, Technology and Education"
SELECT T1.event_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.status = 'Closed' ORDER BY (T2.spent / T2.amount) DESC LIMIT 1
SELECT COUNT(*) FROM member WHERE position = 'President'
SELECT MAX(spent) FROM budget
SELECT COUNT(event_id) FROM event WHERE type = 'Meeting' AND STRFTIME('%Y', event_date) = '2020'
SELECT SUM(spent) FROM budget WHERE category = 'Food'
SELECT T1.first_name, T1.last_name FROM member AS T1 INNER JOIN attendance AS T2 ON T1.member_id = T2.link_to_member GROUP BY T1.member_id HAVING COUNT(T2.link_to_event) > 7
SELECT m.first_name, m.last_name FROM member m JOIN attendance a ON m.member_id = a.link_to_member JOIN event e ON a.link_to_event = e.event_id JOIN major maj ON m.link_to_major = maj.major_id WHERE maj.major_name = 'Interior Design' AND e.event_name = 'Community Theater'
SELECT m.first_name, m.last_name FROM member m JOIN zip_code z ON m.zip = z.zip_code WHERE z.city = 'Georgetown' AND z.state = 'South Carolina'
SELECT SUM(i.amount) AS total_income FROM income i JOIN member m ON i.link_to_member = m.member_id WHERE m.first_name = 'Grant' AND m.last_name = 'Gilmour'
SELECT m.first_name, m.last_name FROM member m JOIN income i ON m.member_id = i.link_to_member WHERE i.amount > 40
SELECT SUM(T3.cost) FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event INNER JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget WHERE T1.event_name = 'Yearly Kickoff'
SELECT DISTINCT T4.first_name ,  T4.last_name FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event INNER JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget INNER JOIN member AS T4 ON T3.link_to_member = T4.member_id WHERE T1.event_name = 'Yearly Kickoff'
SELECT m.first_name, m.last_name, i.source FROM income i JOIN member m ON i.link_to_member = m.member_id ORDER BY i.amount DESC LIMIT 1
SELECT e.event_name FROM event e JOIN budget b ON e.event_id = b.link_to_event JOIN expense ex ON b.budget_id = ex.link_to_budget GROUP BY e.event_name ORDER BY MIN(ex.cost) ASC LIMIT 1
SELECT CAST(SUM(CASE WHEN T1.event_name = 'Yearly Kickoff' THEN T3.cost ELSE 0 END) AS REAL) * 100 / NULLIF(SUM(T3.cost), 0) AS percentage FROM event AS T1 INNER JOIN budget AS T2 ON T2.link_to_event = T1.event_id INNER JOIN expense AS T3 ON T3.link_to_budget = T2.budget_id
SELECT CAST(SUM(CASE WHEN T1.major_name = 'Finance' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN T1.major_name = 'Physics' THEN 1 ELSE 0 END) AS ratio FROM major AS T1 JOIN member AS T2 ON T1.major_id = T2.link_to_major
SELECT source FROM income WHERE date_received BETWEEN '2019-09-01' AND '2019-09-30' GROUP BY source ORDER BY SUM(amount) DESC LIMIT 1
SELECT first_name, last_name, email FROM member WHERE position = 'Secretary'
SELECT COUNT(*) FROM member JOIN major ON member.link_to_major = major.major_id WHERE major.major_name = 'Physics Teaching'
SELECT COUNT(T2.link_to_member) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_name = 'Community Theater' AND STRFTIME('%Y', T1.event_date) = '2019'
SELECT (SELECT COUNT(*) FROM attendance WHERE link_to_member = (SELECT member_id FROM member WHERE first_name = 'Luisa' AND last_name = 'Guidi')) AS number_of_events_attended, (SELECT major_name FROM major WHERE major_id = (SELECT link_to_major FROM member WHERE first_name = 'Luisa' AND last_name = 'Guidi')) AS major
SELECT SUM(spent) / COUNT(spent) AS average_spent FROM budget WHERE category = 'Food' AND event_status = 'Closed'
SELECT T1.event_name FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T2.category = 'Advertisement' ORDER BY T2.spent DESC LIMIT 1
SELECT CASE WHEN EXISTS ( SELECT 1 FROM member m JOIN attendance a ON m.member_id = a.link_to_member JOIN event e ON a.link_to_event = e.event_id WHERE m.first_name = 'Maya' AND m.last_name = 'Mclean' AND e.event_name = 'Women''s Soccer' ) THEN 'Yes' ELSE 'No' END AS attended
SELECT (SUM(CASE WHEN type = 'Community Service' THEN 1 ELSE 0 END) * 100.0 / COUNT(event_id)) AS community_service_percentage FROM event WHERE event_date BETWEEN '2019-01-01' AND '2019-12-31'
SELECT e.cost FROM expense e JOIN budget b ON e.link_to_budget = b.budget_id JOIN event ev ON b.link_to_event = ev.event_id WHERE ev.event_name = 'September Speaker' AND e.expense_description = 'Posters'
SELECT t_shirt_size FROM member GROUP BY t_shirt_size ORDER BY COUNT(*) DESC LIMIT 1
SELECT T1.event_name FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.status = 'Closed' AND T2.remaining < 0 ORDER BY T2.remaining ASC LIMIT 1
SELECT T3.expense_description, CAST(SUM(T3.cost) AS REAL) FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event INNER JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget WHERE T1.event_name = 'October Meeting' AND T3.approved = 'true' GROUP BY T3.expense_description ORDER BY T3.expense_description
SELECT b.category, b.amount FROM event e JOIN budget b ON e.event_id = b.link_to_event WHERE e.event_name = 'April Speaker' ORDER BY b.amount ASC
SELECT MAX(amount) FROM budget WHERE category = 'Food'
SELECT amount FROM budget WHERE category = 'Advertisement' ORDER BY amount DESC LIMIT 3
SELECT SUM(cost) FROM expense WHERE expense_description = 'Parking'
SELECT SUM(cost) AS total_expense FROM expense WHERE expense_date = '2019-08-20'
SELECT m.first_name, m.last_name, SUM(e.cost) AS total_cost FROM member m JOIN expense e ON m.member_id = e.link_to_member WHERE m.member_id = 'rec4BLdZHS2Blfp4v' GROUP BY m.first_name, m.last_name
SELECT T2.expense_description FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.first_name = 'Sacha' AND T1.last_name = 'Harrison'
SELECT T2.expense_description FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.t_shirt_size = 'X-Large'
SELECT DISTINCT m.zip FROM member m JOIN expense e ON m.member_id = e.link_to_member WHERE e.cost < 50
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Phillip' AND T1.last_name = 'Cullen'
SELECT T2.position FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major WHERE T1.major_name = 'Business'
SELECT COUNT(*) FROM member m JOIN major mj ON m.link_to_major = mj.major_id WHERE mj.major_name = 'Business' AND m.t_shirt_size = 'Medium'
SELECT T2.type FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T1.remaining > 30
SELECT DISTINCT T1.category FROM budget AS T1 INNER JOIN event AS T2 ON T2.event_id = T1.link_to_event WHERE T2.location = 'MU 215'
SELECT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.event_date = '2020-03-24T12:00:00'
SELECT T2.major_name FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position = 'Vice President'
SELECT CAST(SUM(CASE WHEN T2.major_name = 'Business' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.member_id) AS percentage FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id
SELECT DISTINCT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.location = 'MU 215'
SELECT COUNT(*) FROM income WHERE amount = 50
SELECT COUNT(member_id) FROM member WHERE t_shirt_size = 'X-Large' AND position = 'Member'
SELECT COUNT(*) FROM major WHERE college = 'College of Agriculture and Applied Sciences' AND department = 'School of Applied Sciences, Technology and Education'
SELECT T1.last_name, T2.department, T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Environmental Engineering'
SELECT T2.category FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T1.location = 'MU 215' AND T1.type = 'Guest Speaker' AND T2.spent = 0
SELECT z.city, z.state FROM member m JOIN major ma ON m.link_to_major = ma.major_id JOIN zip_code z ON m.zip = z.zip_code WHERE ma.department = 'Electrical and Computer Engineering Department' AND m.position = 'Member'
SELECT e.event_name FROM event e JOIN attendance a ON e.event_id = a.link_to_event JOIN member m ON a.link_to_member = m.member_id WHERE e.type = 'Social' AND e.location = '900 E. Washington St.' AND m.position = 'Vice President'
SELECT T2.last_name, T2.position FROM expense AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.expense_description = 'Pizza' AND T1.expense_date = '2019-09-10'
SELECT T2.last_name FROM attendance AS T1 JOIN member AS T2 ON T1.link_to_member = T2.member_id JOIN event AS T3 ON T1.link_to_event = T3.event_id WHERE T3.event_name = 'Women''s Soccer' AND T2.position = 'Member'
SELECT CAST(COUNT(CASE WHEN T2.amount = 50 THEN 1 END) AS REAL) * 100 / COUNT(*) FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.t_shirt_size = 'Medium' AND T1.position = 'Member'
SELECT DISTINCT county FROM zip_code WHERE type = 'PO Box'
SELECT zip_code FROM zip_code WHERE county = 'San Juan Municipio' AND state = 'Puerto Rico' AND type = 'PO Box'
SELECT event_name FROM event WHERE type = 'Game' AND status = 'Closed' AND event_date BETWEEN '2019-03-15' AND '2020-03-20'
SELECT T1.link_to_event FROM budget AS T1 INNER JOIN expense AS T2 ON T1.budget_id = T2.link_to_budget WHERE T2.cost > 50
SELECT T2.link_to_member, T2.link_to_event FROM expense AS T1 INNER JOIN attendance AS T2 ON T1.link_to_member = T2.link_to_member INNER JOIN member AS T3 ON T2.link_to_member = T3.member_id WHERE T1.approved = 'true' AND T1.expense_date BETWEEN '2019-01-10' AND '2019-11-19'
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Katy' AND T1.link_to_major = 'rec1N0upiVLy5esTO'
SELECT T1.phone FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Business' AND T2.college = 'College of Agriculture and Applied Sciences'
SELECT T2.email FROM expense AS T1 JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T1.expense_date BETWEEN '2019-09-10' AND '2019-11-19' AND T1.cost > 20
SELECT COUNT(*) FROM member m JOIN major ma ON m.link_to_major = ma.major_id WHERE m.position = 'Member' AND ma.major_name = 'education' AND ma.college = 'College of Education & Human Services'
SELECT CAST(COUNT(CASE WHEN T2.remaining < 0 THEN T1.event_id ELSE NULL END) AS REAL) * 100 / COUNT(T1.event_id) FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event
SELECT event_id, location, status FROM event WHERE event_date BETWEEN '2019-11-01' AND '2020-03-31'
SELECT expense_description FROM expense GROUP BY expense_description HAVING AVG(cost) > 50
SELECT first_name, last_name FROM member WHERE t_shirt_size = 'X-Large'
SELECT CAST(SUM(CASE WHEN type = 'PO Box' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(zip_code) FROM zip_code
SELECT T1.event_name, T1.location FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event WHERE T2.remaining > 0
SELECT T1.event_name, T1.event_date FROM event AS T1 JOIN budget AS T2 ON T1.event_id = T2.link_to_event JOIN expense AS T3 ON T2.budget_id = T3.link_to_budget WHERE T3.expense_description = 'Pizza' AND T3.cost > 50 AND T3.cost < 100
SELECT T1.first_name, T1.last_name, T2.major_name FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id JOIN expense AS T3 ON T1.member_id = T3.link_to_member WHERE T3.cost > 100
SELECT T3.city, T3.state FROM income AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id INNER JOIN zip_code AS T3 ON T2.zip = T3.zip_code WHERE T1.amount > 40
SELECT m.first_name, m.last_name FROM member m JOIN expense e ON m.member_id = e.link_to_member JOIN attendance a ON m.member_id = a.link_to_member GROUP BY m.member_id HAVING COUNT(DISTINCT a.link_to_event) > 1 ORDER BY SUM(e.cost) DESC LIMIT 1
SELECT AVG(e.cost) AS average_amount_paid FROM expense e JOIN member m ON e.link_to_member = m.member_id WHERE m.position != 'Member'
SELECT e.event_name FROM event e JOIN budget b ON e.event_id = b.link_to_event WHERE b.category = 'Parking' AND b.spent < (SELECT AVG(spent) FROM budget WHERE category = 'Parking')
SELECT (SUM(e.cost) / COUNT(ev.event_id)) * 100 AS percentage FROM event ev JOIN budget b ON ev.event_id = b.link_to_event JOIN expense e ON b.budget_id = e.link_to_budget WHERE ev.type = 'Meeting'
SELECT link_to_budget FROM expense WHERE cost = ( SELECT MAX(cost) FROM expense WHERE expense_description = 'Water, chips, cookies' ) AND expense_description = 'Water, chips, cookies'
SELECT m.first_name, m.last_name FROM member m JOIN expense e ON m.member_id = e.link_to_member GROUP BY m.member_id ORDER BY SUM(e.cost) DESC LIMIT 5
SELECT DISTINCT m.first_name, m.last_name, m.phone FROM expense e JOIN member m ON e.link_to_member = m.member_id WHERE e.cost > (SELECT AVG(cost) FROM expense)
SELECT (SUM(CASE WHEN T2.state = 'New Jersey' THEN 1 ELSE 0 END) * 1.0 / COUNT(T1.member_id)) - (SUM(CASE WHEN T2.state = 'Vermont' THEN 1 ELSE 0 END) * 1.0 / COUNT(T1.member_id)) AS percentage_difference FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.position = 'Member'
SELECT T2.major_name, T2.department FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.first_name = 'Garrett' AND T1.last_name = 'Gerke'
SELECT m.first_name, m.last_name, e.cost FROM member m JOIN expense e ON m.member_id = e.link_to_member WHERE e.expense_description = 'Water, Veggie tray, supplies'
SELECT T1.last_name, T1.phone FROM member AS T1 JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T2.major_name = 'Elementary Education'
SELECT budget.category, budget.amount FROM event JOIN budget ON event.event_id = budget.link_to_event WHERE event.event_name = 'January Speaker'
SELECT e.event_name FROM event e JOIN budget b ON e.event_id = b.link_to_event WHERE b.category = 'Food'
SELECT T1.first_name, T1.last_name, T2.amount FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T2.date_received = '2019-09-09'
SELECT T1.category FROM budget AS T1 INNER JOIN expense AS T2 ON T1.budget_id = T2.link_to_budget WHERE T2.expense_description = 'Posters'
SELECT m.first_name, m.last_name, ma.college FROM member m JOIN major ma ON m.link_to_major = ma.major_id WHERE m.position = 'Secretary'
SELECT SUM(b.spent) AS total_amount_spent, e.event_name FROM budget b JOIN event e ON b.link_to_event = e.event_id WHERE b.category = 'Speaker Gifts'
SELECT T2.city FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T1.first_name = 'Garrett' AND T1.last_name = 'Gerke'
SELECT T1.first_name, T1.last_name, T1.position FROM member AS T1 INNER JOIN zip_code AS T2 ON T1.zip = T2.zip_code WHERE T2.zip_code = 28092 AND T2.city = 'Lincolnton' AND T2.state = 'North Carolina'
SELECT COUNT(*) FROM gasstations WHERE Country = 'CZE' AND Segment = 'Premium'
SELECT CAST(COUNT(CASE WHEN Currency = 'EUR' THEN 1 ELSE NULL END) AS REAL) / COUNT(CASE WHEN Currency = 'CZK' THEN 1 ELSE NULL END) AS ratio_EUR_to_CZK FROM customers
SELECT c.CustomerID FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Segment = 'LAM' AND y.Date LIKE '2012%' ORDER BY y.Consumption ASC LIMIT 1
SELECT AVG(Consumption) / 12 AS average_monthly_consumption FROM yearmonth JOIN customers ON yearmonth.CustomerID = customers.CustomerID WHERE customers.Segment = 'SME' AND yearmonth.Date LIKE '2013%'
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'CZK' AND T2.Date BETWEEN '201101' AND '201112' GROUP BY T1.CustomerID ORDER BY SUM(T2.Consumption) DESC LIMIT 1
SELECT COUNT(CustomerID) FROM ( SELECT c.CustomerID FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Segment = 'KAM' AND y.Date BETWEEN '201201' AND '201212' GROUP BY c.CustomerID HAVING SUM(y.Consumption) < 30000 ) AS kam_customers
SELECT SUM(CASE WHEN c.Currency = 'CZK' THEN y.Consumption ELSE 0 END) - SUM(CASE WHEN c.Currency = 'EUR' THEN y.Consumption ELSE 0 END) AS DifferenceInConsumption FROM yearmonth y JOIN customers c ON y.CustomerID = c.CustomerID WHERE y.Date BETWEEN '201201' AND '201212'
SELECT STRFTIME('%Y', T1.Date) FROM ( SELECT t.Date, SUM(t.Amount) as total_amount FROM transactions_1k t JOIN customers c ON t.CustomerID = c.CustomerID WHERE c.Currency = 'EUR' GROUP BY STRFTIME('%Y', t.Date) ) as T1 ORDER BY T1.total_amount DESC LIMIT 1
SELECT t2.Segment FROM yearmonth AS t1 INNER JOIN customers AS t2 ON t1.CustomerID = t2.CustomerID GROUP BY t2.Segment ORDER BY SUM(t1.Consumption) ASC LIMIT 1
SELECT SUBSTR(T1.Date, 1, 4) AS Year FROM yearmonth AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Currency = 'CZK' GROUP BY SUBSTR(T1.Date, 1, 4) ORDER BY SUM(T1.Consumption) DESC LIMIT 1
SELECT SUBSTR(ym.Date, 5, 2) AS peak_month FROM yearmonth ym JOIN customers c ON ym.CustomerID = c.CustomerID WHERE ym.Date BETWEEN '201301' AND '201312' AND c.Segment = 'SME' GROUP BY SUBSTR(ym.Date, 5, 2) ORDER BY SUM(ym.Consumption) DESC LIMIT 1
WITH lowest_consumption_customers AS (     SELECT         ym.CustomerID,         ym.`Date`,         ym.Consumption,         c.Segment,         ROW_NUMBER() OVER (PARTITION BY c.Segment ORDER BY ym.Consumption ASC) AS rn     FROM         yearmonth ym     JOIN         customers c ON ym.CustomerID = c.CustomerID     WHERE         ym.`Date` BETWEEN '201301' AND '201312' ), segment_consumption AS (     SELECT         lcc.Segment,         SUM(lcc.Consumption) AS TotalConsumption,         COUNT(lcc.CustomerID) AS NumberOfCustomers     FROM         lowest_consumption_customers lcc     WHERE         lcc.rn = 1     GROUP BY         lcc.Segment ) SELECT     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'SME') -     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'LAM') AS SME_LAM_Difference,     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'LAM') -     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'KAM') AS LAM_KAM_Difference,     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'KAM') -     (SELECT TotalConsumption / NumberOfCustomers FROM segment_consumption WHERE Segment = 'SME') AS KAM_SME_Difference
SELECT Segment, (SUM(CASE WHEN SUBSTR(y.Date, 1, 4) = '2013' THEN y.Consumption ELSE 0 END) - SUM(CASE WHEN SUBSTR(y.Date, 1, 4) = '2012' THEN y.Consumption ELSE 0 END)) / SUM(CASE WHEN SUBSTR(y.Date, 1, 4) = '2013' THEN y.Consumption ELSE 0 END) * 100 AS PercentageIncrease FROM yearmonth y JOIN customers c ON y.CustomerID = c.CustomerID WHERE c.Currency = 'EUR' AND y.Date IN (SELECT Date FROM yearmonth WHERE Date LIKE '2012%' OR Date LIKE '2013%')
SELECT SUM(Consumption) FROM yearmonth WHERE CustomerID = 6 AND Date BETWEEN '201308' AND '201311'
SELECT COUNT(CASE WHEN Country = 'CZE' AND Segment = 'Discount' THEN 1 END) - COUNT(CASE WHEN Country = 'SVK' AND Segment = 'Discount' THEN 1 END) AS Difference FROM gasstations
SELECT (SELECT Consumption FROM yearmonth WHERE CustomerID = 7 AND Date = '201304') - (SELECT Consumption FROM yearmonth WHERE CustomerID = 5 AND Date = '201304') AS Difference
SELECT SUM(CASE WHEN T2.Currency = 'CZK' THEN T1.Amount ELSE 0 END) - SUM(CASE WHEN T2.Currency = 'EUR' THEN T1.Amount ELSE 0 END) AS AmountDifference FROM transactions_1k AS T1 JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Segment = 'SME'
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'LAM' AND T1.Currency = 'EUR' AND T2.Date = '201310' ORDER BY T2.Consumption DESC LIMIT 1
SELECT T1.CustomerID, SUM(T2.Consumption) AS TotalConsumption FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'KAM' GROUP BY T1.CustomerID ORDER BY TotalConsumption DESC LIMIT 1
SELECT SUM(T2.Consumption) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'KAM' AND T2.Date = '201305'
SELECT (SUM(CASE WHEN y.Consumption > 46.73 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Segment = 'LAM'
SELECT Country, COUNT(*) AS Total_Value_for_Money_GasStations FROM gasstations WHERE Segment = 'Value for money' GROUP BY Country
SELECT CAST(SUM(CASE WHEN Currency = 'EUR' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(CustomerID) AS Percentage FROM customers WHERE Segment = 'KAM'
SELECT (SUM(CASE WHEN Consumption > 528.3 THEN 1 ELSE 0 END) * 100.0 / COUNT(CustomerID)) AS percentage FROM yearmonth WHERE Date = '201202'
SELECT (SUM(CASE WHEN Segment = 'Premium' THEN 1 ELSE 0 END) * 100.0 / COUNT(GasStationID)) AS PremiumPercentage FROM gasstations WHERE Country = 'SVK'
SELECT CustomerID FROM yearmonth WHERE Date = '201309' ORDER BY Consumption DESC LIMIT 1
SELECT c.Segment FROM customers c JOIN yearmonth ym ON c.CustomerID = ym.CustomerID WHERE ym.Date = '201309' GROUP BY c.Segment ORDER BY SUM(ym.Consumption) ASC LIMIT 1
SELECT y.CustomerID FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Segment = 'SME' AND y.Date = '201206' ORDER BY y.Consumption ASC LIMIT 1
SELECT MAX(Consumption) FROM yearmonth WHERE Date LIKE '2012%'
SELECT MAX(y.Consumption / 12) AS BiggestMonthlyConsumption FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Currency = 'EUR'
SELECT DISTINCT T3.Description FROM yearmonth AS T1 INNER JOIN transactions_1k AS T2 ON T1.CustomerID = T2.CustomerID INNER JOIN products AS T3 ON T2.ProductID = T3.ProductID WHERE SUBSTR(T1.Date, 1, 6) = '201309'
SELECT DISTINCT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID INNER JOIN yearmonth AS T3 ON T1.CustomerID = T3.CustomerID WHERE T3.Date = '201306'
SELECT DISTINCT gs.ChainID FROM transactions_1k t JOIN customers c ON t.CustomerID = c.CustomerID JOIN gasstations gs ON t.GasStationID = gs.GasStationID WHERE c.Currency = 'EUR'
SELECT p.Description FROM customers c JOIN transactions_1k t ON c.CustomerID = t.CustomerID JOIN products p ON t.ProductID = p.ProductID WHERE c.Currency = 'EUR'
SELECT AVG(T1.Price) FROM transactions_1k AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date LIKE '201201'
SELECT COUNT(DISTINCT T1.CustomerID) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR' AND T2.Consumption > 1000
SELECT DISTINCT T3.Description FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID INNER JOIN products AS T3 ON T1.ProductID = T3.ProductID WHERE T2.Country = 'CZE'
SELECT T2.Time FROM gasstations AS T1 INNER JOIN transactions_1k AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.ChainID = 11
SELECT COUNT(T1.TransactionID) FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T2.Country = 'CZE' AND T1.Price > 1000
SELECT COUNT(*) FROM transactions_1k t JOIN gasstations g ON t.GasStationID = g.GasStationID WHERE g.Country = 'CZE' AND t.Date > '2012-01-01'
SELECT AVG(t1.Amount * t1.Price) AS average_total_price FROM transactions_1k AS t1 JOIN gasstations AS t2 ON t1.GasStationID = t2.GasStationID WHERE t2.Country = 'CZE'
SELECT AVG(t.Price) AS average_total_price FROM transactions_1k t JOIN customers c ON t.CustomerID = c.CustomerID WHERE c.Currency = 'EUR'
SELECT CustomerID FROM transactions_1k WHERE `Date` = '2012-08-25' ORDER BY Amount DESC LIMIT 1
SELECT g.Country FROM gasstations g JOIN (SELECT GasStationID       FROM transactions_1k       WHERE Date = '2012-08-25'       ORDER BY Time ASC       LIMIT 1) t ON g.GasStationID = t.GasStationID
SELECT T2.Currency FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '2012-08-24' AND T1.Time = '16:25:00'
SELECT Segment FROM transactions_1k JOIN customers ON transactions_1k.CustomerID = customers.CustomerID WHERE transactions_1k.Date = '2012-08-23' AND transactions_1k.Time = '21:20:00'
SELECT COUNT(*) FROM transactions_1k t JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.Date = '2012-08-26' AND t.Time < '13:00:00' AND c.Currency = 'CZK'
SELECT Segment FROM customers ORDER BY CustomerID ASC LIMIT 1
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-24' AND T1.Time = '12:42:00'
SELECT ProductID FROM transactions_1k WHERE `Date` = '2012-08-23' AND `Time` = '21:20:00'
SELECT T2.`Date`, T2.Consumption FROM transactions_1k AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.`Date` = '2012-08-24' AND T1.Price = 124.05 AND T2.`Date` LIKE '201201'
SELECT COUNT(*) FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-26' AND T1.Time BETWEEN '08:00:00' AND '09:00:00' AND T2.Country = 'CZE'
SELECT T1.Currency FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date = '201306' AND T2.Consumption = 214582.17
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID INNER JOIN customers AS T3 ON T1.CustomerID = T3.CustomerID WHERE T1.CardID = 667467
SELECT T2.Currency FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '2012-08-24' AND T1.Price = 548.4
SELECT (SUM(IIF(T2.Currency = 'EUR', 1, 0)) * 100.0 / COUNT(*)) AS PercentageEUR FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '2012-08-25'
SELECT (t2012.Consumption - t2013.Consumption) / t2012.Consumption AS DecreaseRate FROM ( SELECT Consumption FROM yearmonth WHERE CustomerID IN ( SELECT CustomerID FROM transactions_1k WHERE `Date` = '2012-08-25' AND Amount = 634.8 ) AND `Date` = '201212' ) t2012, ( SELECT Consumption FROM yearmonth WHERE CustomerID IN ( SELECT CustomerID FROM transactions_1k WHERE `Date` = '2012-08-25' AND Amount = 634.8 ) AND `Date` = '201312' ) t2013
SELECT T.GasStationID  FROM (     SELECT T1.GasStationID, SUM(T1.Amount * T1.Price) AS Revenue      FROM transactions_1k AS T1      INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID      GROUP BY T1.GasStationID      ORDER BY Revenue DESC      LIMIT 1 ) AS T
SELECT (SELECT COUNT(*) FROM gasstations WHERE Country = "SVK" AND Segment = "Premium") * 100.0 / (SELECT COUNT(*) FROM gasstations WHERE Country = "SVK") AS PremiumPercentage
SELECT SUM(t1.Amount) FROM transactions_1k AS t1 INNER JOIN yearmonth AS t2 ON t1.CustomerID = t2.CustomerID WHERE t1.CustomerID = 38508 AND t2.Date = '201201'
SELECT p.Description FROM transactions_1k t JOIN products p ON t.ProductID = p.ProductID GROUP BY t.ProductID ORDER BY COUNT(t.TransactionID) DESC LIMIT 5
SELECT      t.CustomerID,      (SUM(t.Price) / SUM(t.Amount)) AS average_price_per_item,      c.Currency FROM      transactions_1k t JOIN      customers c ON t.CustomerID = c.CustomerID WHERE      t.CustomerID = (         SELECT              CustomerID          FROM              transactions_1k          GROUP BY              CustomerID          ORDER BY              SUM(Price) DESC          LIMIT 1     ) GROUP BY      t.CustomerID, c.Currency
SELECT g.Country FROM gasstations g JOIN transactions_1k t ON g.GasStationID = t.GasStationID WHERE t.ProductID = 2 ORDER BY t.Price DESC LIMIT 1
SELECT y.Consumption FROM transactions_1k t JOIN yearmonth y ON t.CustomerID = y.CustomerID WHERE t.ProductID = 5 AND t.Price / t.Amount > 29.00 AND y.Date = '201208'