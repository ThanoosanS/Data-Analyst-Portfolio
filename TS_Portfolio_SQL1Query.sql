-- Total Cases in Canada
-- Uses WHERE, ORDER BY 
SELECT Location, date, total_cases, new_cases 
FROM Portfolio..CovidDeaths
WHERE Location = 'Canada'
ORDER by date 


-- Maximum number of Cases in one day (Canada) 
-- Uses MAX aggregate function
SELECT Location, MAX(new_Cases) as MaxCasesCanada
FROM Portfolio..CovidDeaths
WHERE Location = 'Canada'
GROUP BY Location


-- Total Deaths vs Total Cases in Canada (Likelihood of dying if contracting COVID in Canada)
-- Uses Arithmetic Operators, CAST Function
SELECT Location, date, CAST(total_cases AS INT) AS totalCases, 
CAST(total_Deaths AS INT) AS totalDeaths, 
(CAST(total_deaths AS FLOAT)/CAST(total_cases AS FLOAT))*100 AS DeathPercent
FROM Portfolio..CovidDeaths
WHERE Location = 'Canada'
Order by Location, date


-- Total Cases vs Population in Canada
SELECT Location, date, population, new_cases, total_cases, (CAST(total_Cases AS FLOAT)/population)*100 CasesPercent 
FROM Portfolio..CovidDeaths
WHERE Location = 'Canada'
ORDER BY 1,2


-- Countries with highest infection rates (Top 100)
-- Uses ORDER DESC, TOP (LIMIT)
SELECT TOP 100 Location, population, MAX(total_cases) AS highestInfectionCount, (MAX(CAST(total_cases AS FLOAT))/population)*100 AS PercentPopInfected
FROM Portfolio..CovidDeaths
GROUP BY Location, population
ORDER BY PercentPopInfected DESC


-- Showing Top 100 Countries with Highest Death Count per Pop
-- Uses NOT NULL
SELECT TOP 100 Location, MAX(CAST(total_Deaths AS INT)) AS TotalDeathCount
FROM Portfolio..CovidDeaths
WHERE Continent IS NOT NULL -- Filters out continents
GROUP BY Location, population
ORDER BY TotalDeathCount DESC


-- Showing Top Continents with highest Death Counts 
-- Uses NOT LIKE, AND
SELECT Location, MAX(CAST(total_Deaths AS INT)) AS totalDeathCount
FROM Portfolio..CovidDeaths
WHERE continent IS NULL AND Location NOT LIKE '%income' --Filter out high, medium, low income 
GROUP BY Location
ORDER BY totalDeathCount DESC


-- Global Death Percentage (total deaths/cases)
SELECT SUM(new_cases) AS totalCases, SUM(new_deaths) AS totalDeaths, SUM(new_deaths)/SUM(new_cases)*100 AS DeathPercentage
FROM Portfolio..CovidDeaths
WHERE Continent IS NOT NULL


-- Global Death Percentage (total deaths/population)
SELECT SUM(population) AS pop, SUM(new_deaths) AS totalDeaths, SUM(new_deaths)/SUM(population)*100 AS DeathPercentage
FROM Portfolio..CovidDeaths
WHERE Continent IS NOT NULL


-- Looking at Total Population vs Vaccines
-- Uses Joins, Aliasing, Partition By (Rolling number per country), BIGINT
SELECT deaths.continent, deaths. location, deaths.date, deaths.population, vaccines.new_vaccinations, 
SUM(CAST(vaccines.new_vaccinations AS BIGINT)) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS RollingPeopleVac 
FROM Portfolio..CovidDeaths deaths
JOIN Portfolio..CovidVac vaccines
	ON deaths.location = vaccines.location
	AND deaths.date = vaccines.date 
WHERE deaths.continent IS NOT NULL
Order by deaths.location, deaths.date


-- CTE of previous Query
-- Uses CTE
WITH PopVac(continent, location, date, population, new_vaccinations, RollingPeopleVac)
AS
(
SELECT deaths.continent, deaths. location, deaths.date, deaths.population, vaccines.new_vaccinations, 
SUM(CAST(vaccines.new_vaccinations AS BIGINT)) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS RollingPeopleVac
FROM Portfolio..CovidDeaths deaths
JOIN Portfolio..CovidVac vaccines
	ON deaths.location = vaccines.location
	AND deaths.date = vaccines.date 
WHERE deaths.continent IS NOT NULL
)
SELECT *, (RollingPeopleVac/population)*100 AS PopulationPercentVac
FROM PopVac


-- Temp Table of previous Query
-- Uses Temp Table, Create Table, Drop Table
DROP TABLE IF EXISTS #PercentPopVaccinated
CREATE TABLE #PercentPopVaccinated
(
continent NVARCHAR(255), 
location NVARCHAR(255), 
date DATETIME, 
population NUMERIC,
new_vaccinations NUMERIC,
RollingPeopleVac NUMERIC
)
INSERT INTO #PercentPopVaccinated
SELECT deaths.continent, deaths. location, deaths.date, deaths.population, vaccines.new_vaccinations, 
SUM(CAST(vaccines.new_vaccinations AS BIGINT)) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS RollingPeopleVac
FROM Portfolio..CovidDeaths deaths
JOIN Portfolio..CovidVac vaccines
	ON deaths.location = vaccines.location
	AND deaths.date = vaccines.date 
WHERE deaths.continent IS NOT NULL

SELECT *, (RollingPeopleVac/population)*100 AS PopulationPercentVac
FROM #PercentPopVaccinated


-- Creating View to store data for later (visualization)
-- Used top 100 Countries with highest deathcount as View
CREATE VIEW TopCountries AS
SELECT TOP 100 Location, MAX(CAST(total_Deaths AS INT)) AS TotalDeathCount
FROM Portfolio..CovidDeaths
WHERE Continent IS NOT NULL -- Filters out continents
GROUP BY Location, population
