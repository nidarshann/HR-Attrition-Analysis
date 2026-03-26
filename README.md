# HR Attrition Analysis
### End-to-End Data Analytics Portfolio Project

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Excel](https://img.shields.io/badge/Excel-xlsx-green) ![SQL](https://img.shields.io/badge/SQL-PostgreSQL-orange) ![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)

---

## Project Overview

This project performs a comprehensive analysis of employee attrition using the IBM HR Analytics dataset (1,470 employees). The goal is to identify the key drivers of employee turnover and deliver actionable HR recommendations.

**Tools Used:** Excel · SQL · Python (pandas, matplotlib, seaborn) · Power BI

---

## Business Problem

> *"Our company is losing employees at an increasing rate. HR needs to understand who is leaving, why they are leaving, and what we can do to retain them."*

---

## Dataset

- **Source:** IBM HR Analytics Employee Attrition & Performance
- **Records:** 1,470 employees
- **Columns:** 32 features (demographics, job info, satisfaction scores)
- **Target Variable:** `Attrition` (Yes / No)

---

## Project Structure

```
hr_attrition_project/
│
├── 1_data/
│   └── IBM_HR_Attrition_Raw.csv          # Raw dataset
│
├── 2_excel/
│   └── HR_Attrition_Analysis.xlsx        # 6-sheet Excel workbook
│       ├── 1_Raw_Data                    # Full dataset with conditional formatting
│       ├── 2_Data_Cleaning               # Quality check log
│       ├── 3_KPI_Dashboard               # Key metrics overview
│       ├── 4_EDA_Pivots                  # 10 pivot tables
│       ├── 5_Business_Insights           # Findings & recommendations
│       └── 6_Cleaned_Data                # Clean data for Power BI import
│
├── 3_sql/
│   └── hr_attrition_queries.sql          # 8 sections of SQL queries
│       ├── Table creation                # CREATE TABLE statement
│       ├── Data quality checks           # NULL / duplicate validation
│       ├── KPI queries                   # Attrition rate, avg income, tenure
│       ├── Breakdown queries             # By dept, role, gender, OT, travel
│       ├── Age band analysis             # CASE WHEN segmentation
│       ├── Window functions              # RANK, running totals
│       ├── Risk scoring CTE              # Multi-factor risk flagging
│       └── Power BI view                 # CREATE VIEW for direct import
│
├── 4_python/
│   ├── hr_attrition_eda.py               # Full EDA script (8 charts)
│   └── charts/
│       ├── 01_attrition_donut.png
│       ├── 02_attrition_by_dept.png
│       ├── 03_overtime_attrition.png
│       ├── 04_income_distribution.png
│       ├── 05_satisfaction_heatmap.png
│       ├── 06_attrition_by_tenure.png
│       ├── 07_correlation_matrix.png
│       └── 08_risk_factors.png
│
├── 5_powerbi/
│   └── POWERBI_SETUP_GUIDE.md            # Step-by-step Power BI instructions
│
└── 6_docs/
    └── README.md                         # This file
```

---

## Key Findings

| # | Finding | Attrition Rate | Business Impact |
|---|---------|---------------|-----------------|
| 1 | Employees on overtime | ~20% | Burnout → 2× resignation risk |
| 2 | Tenure 0-2 years | ~28% | Recruiting investment wasted |
| 3 | Job satisfaction 1-2 | ~30% | Disengagement + culture risk |
| 4 | No stock options | ~25% | Talent lost to equity-offering rivals |
| 5 | Frequent business travel | ~28% | Account manager churn risk |
| 6 | Work-life balance = Bad | ~34% | Mental health + productivity cost |

---

## How to Run

### Python EDA
```bash
# Install dependencies
pip install pandas matplotlib seaborn openpyxl

# Run EDA script
cd 4_python
python hr_attrition_eda.py
# Outputs: 8 charts saved to 4_python/charts/
```

### SQL Queries
```bash
# Import CSV into your database first
# PostgreSQL example:
psql -d your_database -f 3_sql/hr_attrition_queries.sql

# SQLite example:
sqlite3 hr.db ".import 1_data/IBM_HR_Attrition_Raw.csv hr_attrition"
sqlite3 hr.db < 3_sql/hr_attrition_queries.sql
```

### Excel
- Open `2_excel/HR_Attrition_Analysis.xlsx`
- Navigate sheets using tabs at the bottom
- Sheet `3_KPI_Dashboard` contains the summary view

### Power BI
- Follow instructions in `5_powerbi/POWERBI_SETUP_GUIDE.md`
- Import `2_excel/HR_Attrition_Analysis.xlsx` → Sheet `6_Cleaned_Data`
- Add DAX measures from the guide
- Build 4-page dashboard as specified

---

## Top Recommendations

1. **Cap overtime hours** — Introduce mandatory rest days; hire contractors for peak demand
2. **Strengthen onboarding** — 90-day structured plan + 1-year mentorship for 0-2 yr employees
3. **Quarterly pulse surveys** — Act on bottom-quartile satisfaction scores within 30 days
4. **Introduce ESOP/equity** — Stock options reduce attrition by ~8-10 percentage points
5. **Flexible travel policy** — Compensate frequent flyers; offer work-from-home days post-travel
6. **Flexible work hours** — Mandatory leave utilisation tracking to prevent WLB deterioration

---

## Resume Bullet Points

> **HR Attrition Analysis** | Python · SQL · Excel · Power BI

- Analysed IBM HR dataset (1,470 records) using SQL window functions and CTEs to identify top attrition drivers across departments, roles, and demographics
- Built an end-to-end Python EDA pipeline (pandas + seaborn) generating 8 analytical charts; identified overtime as the strongest attrition predictor (~2× average rate)
- Designed a 6-sheet Excel workbook covering data cleaning, pivot analysis, KPI dashboard, and business recommendations
- Created a 4-page interactive Power BI dashboard with DAX measures and slicers for HR stakeholder self-service reporting

---

## Author

**[Your Name]**
Data Analyst | [LinkedIn URL] | [GitHub URL]

---

*Dataset: IBM HR Analytics Employee Attrition & Performance (Kaggle)*
