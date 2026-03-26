-- ============================================================
-- HR Attrition Analysis — SQL Queries
-- Dataset : IBM HR Attrition (1,470 employees)
-- Database: PostgreSQL / MySQL / SQLite compatible
-- Author  : [Your Name]
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- STEP 1: CREATE TABLE
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hr_attrition (
    EmployeeNumber       INT PRIMARY KEY,
    Age                  INT,
    Gender               VARCHAR(10),
    MaritalStatus        VARCHAR(15),
    Education            INT,
    EducationField       VARCHAR(30),
    Department           VARCHAR(40),
    JobRole              VARCHAR(40),
    JobLevel             INT,
    BusinessTravel       VARCHAR(25),
    OverTime             VARCHAR(5),
    MonthlyIncome        INT,
    PercentSalaryHike    INT,
    StockOptionLevel     INT,
    DistanceFromHome     INT,
    NumCompaniesWorked   INT,
    TotalWorkingYears    INT,
    YearsAtCompany       INT,
    YearsInCurrentRole   INT,
    YearsSinceLastPromotion INT,
    YearsWithCurrManager INT,
    TrainingTimesLastYear INT,
    JobSatisfaction      INT,
    EnvironmentSatisfaction INT,
    WorkLifeBalance      INT,
    RelationshipSatisfaction INT,
    JobInvolvement       INT,
    PerformanceRating    INT,
    Attrition            VARCHAR(5)
);

-- ────────────────────────────────────────────────────────────
-- STEP 2: DATA QUALITY CHECKS
-- ────────────────────────────────────────────────────────────

-- 2a. Total record count
SELECT COUNT(*) AS total_employees FROM hr_attrition;

-- 2b. Check for NULLs across key columns
SELECT
    SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END)             AS null_age,
    SUM(CASE WHEN MonthlyIncome IS NULL THEN 1 ELSE 0 END)   AS null_income,
    SUM(CASE WHEN Department IS NULL THEN 1 ELSE 0 END)      AS null_dept,
    SUM(CASE WHEN Attrition IS NULL THEN 1 ELSE 0 END)       AS null_attrition
FROM hr_attrition;

-- 2c. Distinct attrition values (sanity check)
SELECT Attrition, COUNT(*) AS count FROM hr_attrition GROUP BY Attrition;

-- ────────────────────────────────────────────────────────────
-- STEP 3: KPI QUERIES
-- ────────────────────────────────────────────────────────────

-- 3a. Overall attrition rate
SELECT
    COUNT(*)                                                   AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)        AS total_attrited,
    ROUND(
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    )                                                          AS attrition_rate_pct
FROM hr_attrition;

-- 3b. Average monthly income — attrited vs active
SELECT
    Attrition,
    ROUND(AVG(MonthlyIncome), 0)   AS avg_income,
    ROUND(MIN(MonthlyIncome), 0)   AS min_income,
    ROUND(MAX(MonthlyIncome), 0)   AS max_income,
    COUNT(*)                        AS employee_count
FROM hr_attrition
GROUP BY Attrition
ORDER BY Attrition;

-- 3c. Average tenure — attrited vs active
SELECT
    Attrition,
    ROUND(AVG(YearsAtCompany), 1)         AS avg_years_at_company,
    ROUND(AVG(TotalWorkingYears), 1)      AS avg_total_experience,
    ROUND(AVG(YearsSinceLastPromotion), 1) AS avg_yrs_since_promotion
FROM hr_attrition
GROUP BY Attrition;

-- ────────────────────────────────────────────────────────────
-- STEP 4: ATTRITION BREAKDOWN QUERIES
-- ────────────────────────────────────────────────────────────

-- 4a. Attrition by Department
SELECT
    Department,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY Department
ORDER BY attrition_pct DESC;

-- 4b. Attrition by Job Role
SELECT
    JobRole,
    Department,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY JobRole, Department
ORDER BY attrition_pct DESC;

-- 4c. Attrition by Gender
SELECT
    Gender,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY Gender
ORDER BY attrition_pct DESC;

-- 4d. Attrition by Marital Status
SELECT
    MaritalStatus,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY MaritalStatus
ORDER BY attrition_pct DESC;

-- 4e. Attrition by OverTime
SELECT
    OverTime,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY OverTime
ORDER BY attrition_pct DESC;

-- 4f. Attrition by Business Travel
SELECT
    BusinessTravel,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY BusinessTravel
ORDER BY attrition_pct DESC;

-- 4g. Attrition by Job Satisfaction
SELECT
    JobSatisfaction,
    CASE JobSatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END                                                              AS satisfaction_label,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

-- 4h. Attrition by Work-Life Balance
SELECT
    WorkLifeBalance,
    CASE WorkLifeBalance
        WHEN 1 THEN 'Bad'
        WHEN 2 THEN 'Good'
        WHEN 3 THEN 'Better'
        WHEN 4 THEN 'Best'
    END                                                              AS wlb_label,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;

-- 4i. Attrition by Stock Option Level
SELECT
    StockOptionLevel,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct
FROM hr_attrition
GROUP BY StockOptionLevel
ORDER BY StockOptionLevel;

-- ────────────────────────────────────────────────────────────
-- STEP 5: AGE BAND ANALYSIS (using CASE WHEN)
-- ────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Age BETWEEN 46 AND 60 THEN '46-60'
    END                                                              AS age_band,
    COUNT(*)                                                         AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)              AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS attrition_pct,
    ROUND(AVG(MonthlyIncome), 0)                                     AS avg_income
FROM hr_attrition
GROUP BY age_band
ORDER BY age_band;

-- ────────────────────────────────────────────────────────────
-- STEP 6: ADVANCED — WINDOW FUNCTIONS
-- ────────────────────────────────────────────────────────────

-- 6a. Rank departments by attrition rate
SELECT
    Department,
    attrition_pct,
    RANK() OVER (ORDER BY attrition_pct DESC) AS attrition_rank
FROM (
    SELECT
        Department,
        ROUND(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS attrition_pct
    FROM hr_attrition
    GROUP BY Department
) sub;

-- 6b. Running total of attritions by job role (ordered by rate)
SELECT
    JobRole,
    attrited,
    SUM(attrited) OVER (ORDER BY attrition_pct DESC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM (
    SELECT
        JobRole,
        SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS attrited,
        ROUND(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS attrition_pct
    FROM hr_attrition
    GROUP BY JobRole
) sub;

-- 6c. Employees at HIGH attrition risk (multi-factor flag)
SELECT
    EmployeeNumber,
    Department,
    JobRole,
    Age,
    MonthlyIncome,
    YearsAtCompany,
    OverTime,
    JobSatisfaction,
    WorkLifeBalance,
    (
        CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN JobSatisfaction <= 2 THEN 1 ELSE 0 END +
        CASE WHEN WorkLifeBalance <= 2 THEN 1 ELSE 0 END +
        CASE WHEN YearsAtCompany <= 2 THEN 1 ELSE 0 END +
        CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END +
        CASE WHEN DistanceFromHome > 15 THEN 1 ELSE 0 END
    )                                                          AS risk_score,
    CASE
        WHEN (
            CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END +
            CASE WHEN JobSatisfaction <= 2 THEN 1 ELSE 0 END +
            CASE WHEN WorkLifeBalance <= 2 THEN 1 ELSE 0 END +
            CASE WHEN YearsAtCompany <= 2 THEN 1 ELSE 0 END +
            CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END +
            CASE WHEN DistanceFromHome > 15 THEN 1 ELSE 0 END
        ) >= 4 THEN 'HIGH RISK'
        WHEN (
            CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END +
            CASE WHEN JobSatisfaction <= 2 THEN 1 ELSE 0 END +
            CASE WHEN WorkLifeBalance <= 2 THEN 1 ELSE 0 END +
            CASE WHEN YearsAtCompany <= 2 THEN 1 ELSE 0 END +
            CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END +
            CASE WHEN DistanceFromHome > 15 THEN 1 ELSE 0 END
        ) >= 2 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END                                                        AS attrition_risk
FROM hr_attrition
WHERE Attrition = 'No'
ORDER BY risk_score DESC;

-- 6d. Department-wise avg income vs company avg (gap analysis)
SELECT
    Department,
    ROUND(AVG(MonthlyIncome), 0)                                  AS dept_avg_income,
    ROUND(AVG(AVG(MonthlyIncome)) OVER (), 0)                     AS company_avg_income,
    ROUND(AVG(MonthlyIncome) - AVG(AVG(MonthlyIncome)) OVER (), 0) AS income_gap
FROM hr_attrition
GROUP BY Department
ORDER BY income_gap DESC;

-- ────────────────────────────────────────────────────────────
-- STEP 7: CTE — Multi-factor Attrition Summary
-- ────────────────────────────────────────────────────────────
WITH attrition_summary AS (
    SELECT
        Department,
        JobRole,
        OverTime,
        MaritalStatus,
        COUNT(*)                                                   AS total,
        SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)          AS attrited,
        ROUND(AVG(MonthlyIncome), 0)                               AS avg_income,
        ROUND(AVG(YearsAtCompany), 1)                              AS avg_tenure
    FROM hr_attrition
    GROUP BY Department, JobRole, OverTime, MaritalStatus
),
ranked AS (
    SELECT *,
        ROUND(attrited * 100.0 / total, 1)                        AS attrition_pct,
        RANK() OVER (PARTITION BY Department ORDER BY attrited DESC) AS rank_in_dept
    FROM attrition_summary
    WHERE total >= 10
)
SELECT *
FROM ranked
WHERE rank_in_dept <= 3
ORDER BY Department, rank_in_dept;

-- ────────────────────────────────────────────────────────────
-- STEP 8: EXPORT VIEW FOR POWER BI
-- ────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_hr_attrition_powerbi AS
SELECT
    EmployeeNumber,
    Age,
    CASE
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        ELSE '46-60'
    END                                                            AS AgeBand,
    Gender,
    MaritalStatus,
    Department,
    JobRole,
    JobLevel,
    BusinessTravel,
    OverTime,
    MonthlyIncome,
    CASE
        WHEN MonthlyIncome < 3000  THEN 'Low (<3K)'
        WHEN MonthlyIncome < 6000  THEN 'Mid (3-6K)'
        WHEN MonthlyIncome < 10000 THEN 'High (6-10K)'
        ELSE 'Very High (>10K)'
    END                                                            AS SalaryBand,
    YearsAtCompany,
    CASE
        WHEN YearsAtCompany <= 2  THEN '0-2 yrs'
        WHEN YearsAtCompany <= 5  THEN '3-5 yrs'
        WHEN YearsAtCompany <= 10 THEN '6-10 yrs'
        ELSE '10+ yrs'
    END                                                            AS TenureBand,
    JobSatisfaction,
    EnvironmentSatisfaction,
    WorkLifeBalance,
    StockOptionLevel,
    DistanceFromHome,
    TrainingTimesLastYear,
    PerformanceRating,
    Attrition,
    CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END                  AS AttritionBinary
FROM hr_attrition;
