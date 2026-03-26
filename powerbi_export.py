"""
Power BI Ready CSV Export Script
=================================
Generates 5 clean, pre-aggregated CSV files from the IBM HR dataset.
Import all 5 into Power BI and connect them — no transformations needed.

Run:
    python powerbi_export.py

Output files (saved to ../5_powerbi/exports/):
    1. hr_main.csv            — cleaned employee-level data
    2. hr_attrition_dept.csv  — attrition by department
    3. hr_attrition_role.csv  — attrition by job role
    4. hr_kpi_summary.csv     — headline KPIs
    5. hr_risk_factors.csv    — attrition rates by risk factor
"""

import pandas as pd
import numpy as np
import os

DATA_PATH   = '../1_data/IBM_HR_Attrition_Raw.csv'
OUTPUT_DIR  = '../5_powerbi/exports'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# ── Feature Engineering ──────────────────────────────────────
df['AttritionBinary'] = (df['Attrition'] == 'Yes').astype(int)

df['AgeBand'] = pd.cut(df['Age'],
    bins=[17, 25, 35, 45, 60],
    labels=['18-25', '26-35', '36-45', '46-60'])

df['SalaryBand'] = pd.cut(df['MonthlyIncome'],
    bins=[0, 3000, 6000, 10000, 20001],
    labels=['Low (<3K)', 'Mid (3-6K)', 'High (6-10K)', 'Very High (>10K)'])

df['TenureBand'] = pd.cut(df['YearsAtCompany'],
    bins=[-1, 2, 5, 10, 40],
    labels=['0-2 yrs', '3-5 yrs', '6-10 yrs', '10+ yrs'])

df['JobSatisfactionLabel'] = df['JobSatisfaction'].map(
    {1: '1-Low', 2: '2-Medium', 3: '3-High', 4: '4-Very High'})

df['WLBLabel'] = df['WorkLifeBalance'].map(
    {1: '1-Bad', 2: '2-Good', 3: '3-Better', 4: '4-Best'})

df['RiskScore'] = (
    (df['OverTime'] == 'Yes').astype(int) +
    (df['JobSatisfaction'] <= 2).astype(int) +
    (df['WorkLifeBalance'] <= 2).astype(int) +
    (df['YearsAtCompany'] <= 2).astype(int) +
    (df['StockOptionLevel'] == 0).astype(int) +
    (df['DistanceFromHome'] > 15).astype(int)
)

df['RiskCategory'] = pd.cut(df['RiskScore'],
    bins=[-1, 1, 3, 6],
    labels=['Low Risk', 'Medium Risk', 'High Risk'])

# ── FILE 1: Main Employee Table ─────────────────────────────
drop_cols = ['StandardHours', 'EmployeeCount', 'Over18']
df_main = df.drop(columns=drop_cols, errors='ignore').copy()
df_main['AgeBand']            = df_main['AgeBand'].astype(str)
df_main['SalaryBand']         = df_main['SalaryBand'].astype(str)
df_main['TenureBand']         = df_main['TenureBand'].astype(str)
df_main['JobSatisfactionLabel'] = df_main['JobSatisfactionLabel'].astype(str)
df_main['WLBLabel']           = df_main['WLBLabel'].astype(str)
df_main['RiskCategory']       = df_main['RiskCategory'].astype(str)

df_main.to_csv(f'{OUTPUT_DIR}/hr_main.csv', index=False)
print(f"✓ hr_main.csv — {len(df_main)} rows, {len(df_main.columns)} columns")

# ── FILE 2: Attrition by Department ─────────────────────────
dept_summary = df.groupby('Department').agg(
    TotalEmployees   = ('AttritionBinary', 'count'),
    TotalAttrited    = ('AttritionBinary', 'sum'),
    AttritionRate    = ('AttritionBinary', 'mean'),
    AvgMonthlyIncome = ('MonthlyIncome', 'mean'),
    AvgAge           = ('Age', 'mean'),
    AvgTenure        = ('YearsAtCompany', 'mean'),
    AvgJobSat        = ('JobSatisfaction', 'mean'),
    OvertimeCount    = ('OverTime', lambda x: (x=='Yes').sum())
).reset_index()
dept_summary['ActiveEmployees'] = dept_summary['TotalEmployees'] - dept_summary['TotalAttrited']
dept_summary['AttritionRate']   = dept_summary['AttritionRate'].round(4)
dept_summary['AvgMonthlyIncome']= dept_summary['AvgMonthlyIncome'].round(0).astype(int)
dept_summary['AvgAge']          = dept_summary['AvgAge'].round(1)
dept_summary['AvgTenure']       = dept_summary['AvgTenure'].round(1)
dept_summary['AvgJobSat']       = dept_summary['AvgJobSat'].round(2)

dept_summary.to_csv(f'{OUTPUT_DIR}/hr_attrition_dept.csv', index=False)
print(f"✓ hr_attrition_dept.csv — {len(dept_summary)} rows")

# ── FILE 3: Attrition by Job Role ────────────────────────────
role_summary = df.groupby(['JobRole', 'Department']).agg(
    TotalEmployees   = ('AttritionBinary', 'count'),
    TotalAttrited    = ('AttritionBinary', 'sum'),
    AttritionRate    = ('AttritionBinary', 'mean'),
    AvgMonthlyIncome = ('MonthlyIncome', 'mean'),
    AvgJobSat        = ('JobSatisfaction', 'mean'),
    AvgTenure        = ('YearsAtCompany', 'mean')
).reset_index()
role_summary['ActiveEmployees'] = role_summary['TotalEmployees'] - role_summary['TotalAttrited']
role_summary['AttritionRate']   = role_summary['AttritionRate'].round(4)
role_summary['AvgMonthlyIncome']= role_summary['AvgMonthlyIncome'].round(0).astype(int)
role_summary['AvgJobSat']       = role_summary['AvgJobSat'].round(2)
role_summary['AvgTenure']       = role_summary['AvgTenure'].round(1)
role_summary = role_summary.sort_values('AttritionRate', ascending=False)

role_summary.to_csv(f'{OUTPUT_DIR}/hr_attrition_role.csv', index=False)
print(f"✓ hr_attrition_role.csv — {len(role_summary)} rows")

# ── FILE 4: KPI Summary ──────────────────────────────────────
avg_rate = df['AttritionBinary'].mean()
ot_rate  = (df['OverTime'] == 'Yes').mean()

kpi_data = {
    'KPI': [
        'Total Employees', 'Total Attrited', 'Active Employees',
        'Attrition Rate (%)', 'Avg Monthly Income (₹)', 'Avg Age (yrs)',
        'Avg Tenure (yrs)', 'Overtime Rate (%)', 'OT Attrition Rate (%)',
        'Non-OT Attrition Rate (%)', 'High Risk Employees', 'Avg Job Satisfaction',
        'Avg Work-Life Balance', 'Avg Env Satisfaction'
    ],
    'Value': [
        len(df),
        int(df['AttritionBinary'].sum()),
        int((df['Attrition'] == 'No').sum()),
        round(avg_rate * 100, 2),
        int(df['MonthlyIncome'].mean()),
        round(df['Age'].mean(), 1),
        round(df['YearsAtCompany'].mean(), 1),
        round(ot_rate * 100, 2),
        round(df[df['OverTime']=='Yes']['AttritionBinary'].mean() * 100, 2),
        round(df[df['OverTime']=='No']['AttritionBinary'].mean() * 100, 2),
        int((df['RiskScore'] >= 4).sum()),
        round(df['JobSatisfaction'].mean(), 2),
        round(df['WorkLifeBalance'].mean(), 2),
        round(df['EnvironmentSatisfaction'].mean(), 2),
    ],
    'Category': [
        'Headcount', 'Headcount', 'Headcount',
        'Attrition', 'Compensation', 'Demographics',
        'Tenure', 'OverTime', 'OverTime',
        'OverTime', 'Risk', 'Engagement',
        'Engagement', 'Engagement'
    ]
}

kpi_df = pd.DataFrame(kpi_data)
kpi_df.to_csv(f'{OUTPUT_DIR}/hr_kpi_summary.csv', index=False)
print(f"✓ hr_kpi_summary.csv — {len(kpi_df)} KPIs")

# ── FILE 5: Risk Factors Summary ─────────────────────────────
risk_factors = [
    ('OverTime = Yes',        df[df['OverTime']=='Yes']['AttritionBinary'].mean(),          int((df['OverTime']=='Yes').sum()),        'Workload'),
    ('Marital = Single',      df[df['MaritalStatus']=='Single']['AttritionBinary'].mean(),  int((df['MaritalStatus']=='Single').sum()), 'Personal'),
    ('Job Satisfaction 1-2',  df[df['JobSatisfaction']<=2]['AttritionBinary'].mean(),       int((df['JobSatisfaction']<=2).sum()),     'Engagement'),
    ('Work-Life Balance 1-2', df[df['WorkLifeBalance']<=2]['AttritionBinary'].mean(),       int((df['WorkLifeBalance']<=2).sum()),     'Engagement'),
    ('Tenure 0-2 yrs',        df[df['YearsAtCompany']<=2]['AttritionBinary'].mean(),        int((df['YearsAtCompany']<=2).sum()),      'Tenure'),
    ('No Stock Options',      df[df['StockOptionLevel']==0]['AttritionBinary'].mean(),      int((df['StockOptionLevel']==0).sum()),    'Compensation'),
    ('Frequent Travel',       df[df['BusinessTravel']=='Travel_Frequently']['AttritionBinary'].mean(), int((df['BusinessTravel']=='Travel_Frequently').sum()), 'Travel'),
    ('Env Satisfaction 1-2',  df[df['EnvironmentSatisfaction']<=2]['AttritionBinary'].mean(), int((df['EnvironmentSatisfaction']<=2).sum()), 'Engagement'),
    ('Distance > 15km',       df[df['DistanceFromHome']>15]['AttritionBinary'].mean(),      int((df['DistanceFromHome']>15).sum()),    'Commute'),
    ('Job Level 1',           df[df['JobLevel']==1]['AttritionBinary'].mean(),              int((df['JobLevel']==1).sum()),            'Career'),
]

risk_df = pd.DataFrame(risk_factors, columns=['RiskFactor','AttritionRate','AffectedCount','Category'])
risk_df['AttritionRate']     = risk_df['AttritionRate'].round(4)
risk_df['OverallAttritionRate'] = round(avg_rate, 4)
risk_df['RateVsAvg']         = (risk_df['AttritionRate'] - avg_rate).round(4)
risk_df['RiskLevel']         = risk_df['AttritionRate'].apply(
    lambda x: 'High' if x > avg_rate*1.3 else ('Medium' if x > avg_rate else 'Low'))
risk_df = risk_df.sort_values('AttritionRate', ascending=False)

risk_df.to_csv(f'{OUTPUT_DIR}/hr_risk_factors.csv', index=False)
print(f"✓ hr_risk_factors.csv — {len(risk_df)} risk factors")

print(f"""
╔══════════════════════════════════════════════════════════╗
║        Power BI Export Complete — 5 Files Ready         ║
╠══════════════════════════════════════════════════════════╣
║  📁 Output folder : {OUTPUT_DIR:<38}║
║                                                          ║
║  Files generated:                                        ║
║    1. hr_main.csv            Employee-level data         ║
║    2. hr_attrition_dept.csv  Dept summary                ║
║    3. hr_attrition_role.csv  Role summary                ║
║    4. hr_kpi_summary.csv     14 headline KPIs            ║
║    5. hr_risk_factors.csv    10 risk factor rates        ║
║                                                          ║
║  In Power BI:                                            ║
║    Get Data → Text/CSV → import each file                ║
║    Create relationships on EmployeeNumber & Department   ║
╚══════════════════════════════════════════════════════════╝
""")
