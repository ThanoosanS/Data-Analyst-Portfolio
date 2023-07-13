-- SQL Queries for Top Ranked Canadian Companies based on Revenue in 2019
-- Data acquired from TS_Portfolio_Python4

-- All data
SELECT * FROM Portfolio..CanadianCompanies

-- Ranking Companies headquartered in Toronto
SELECT * 
FROM Portfolio..CanadianCompanies
WHERE Headquarters = 'Toronto' 

-- Ranking all Canadian Banks from least valuable to most
SELECT Name, Headquarters, value 
FROM Portfolio..CanadianCompanies
WHERE Industry='Banking'
ORDER BY value ASC

-- Ranking all industries by combined revenue
SELECT Industry, SUM(Revenue) AS [sum_Revenue(billions US$)]
FROM Portfolio..CanadianCompanies
GROUP BY Industry 
ORDER BY [sum_Revenue(billions US$)] DESC

-- Rank all headquarter locations based on combined value
SELECT Headquarters, SUM(Value) AS [sum_Value(billions US$)]
FROM Portfolio..CanadianCompanies
GROUP BY Headquarters
ORDER BY [sum_Value(billions US$)] DESC
