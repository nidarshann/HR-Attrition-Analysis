"""
HR Attrition Analysis — Python EDA Script
==========================================
Tools   : pandas, matplotlib, seaborn
Dataset : IBM HR Attrition (1,470 employees)
Outputs : 8 charts saved to 4_python/charts/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────────
DATA_PATH   = '../1_data/IBM_HR_Attrition_Raw.csv'
CHARTS_DIR  = 'charts'
os.makedirs(CHARTS_DIR, exist_ok=True)

NAVY   = '#1F3864'
BLUE   = '#2E75B6'
SKY    = '#9DC3E6'
RED    = '#C00000'
AMBER  = '#ED7D31'
GREEN  = '#70AD47'
GRAY   = '#7F7F7F'
LIGHT  = '#D6E4F0'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.titlecolor': NAVY,
    'figure.facecolor': 'white',
    'axes.facecolor': '#F8FAFE',
})

# ── Load & Prepare ────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
df['AttritionBinary'] = (df['Attrition'] == 'Yes').astype(int)
df['AgeBand'] = pd.cut(df['Age'], bins=[17,25,35,45,60],
                       labels=['18-25','26-35','36-45','46-60'])
df['SalaryBand'] = pd.cut(df['MonthlyIncome'],
                          bins=[0,3000,6000,10000,20001],
                          labels=['<3K','3-6K','6-10K','>10K'])
df['TenureBand'] = pd.cut(df['YearsAtCompany'],
                          bins=[-1,2,5,10,40],
                          labels=['0-2','3-5','6-10','10+'])

attr_yes = df[df['Attrition'] == 'Yes']
attr_no  = df[df['Attrition'] == 'No']

print(f"Dataset loaded: {len(df)} employees | Attrition: {df['AttritionBinary'].mean():.1%}")
print("Generating 8 charts...\n")


# ────────────────────────────────────────────────────────────
# CHART 1 — Overall Attrition Donut
# ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
sizes  = [df['AttritionBinary'].sum(), (df['Attrition']=='No').sum()]
labels = [f"Attrited\n{sizes[0]} ({sizes[0]/len(df):.1%})",
          f"Active\n{sizes[1]} ({sizes[1]/len(df):.1%})"]
colors = [RED, GREEN]
wedges, texts = ax.pie(sizes, labels=labels, colors=colors,
                       startangle=90, wedgeprops=dict(width=0.55),
                       textprops={'fontsize': 11})
ax.set_title('Overall Attrition Split\n1,470 Employees', pad=20)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/01_attrition_donut.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 1: Attrition donut")


# ────────────────────────────────────────────────────────────
# CHART 2 — Attrition by Department
# ────────────────────────────────────────────────────────────
dept = df.groupby('Department')['AttritionBinary'].agg(['mean','sum','count']).reset_index()
dept.columns = ['Department','Rate','Attrited','Total']
dept = dept.sort_values('Rate', ascending=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(dept['Department'], dept['Rate']*100,
               color=[RED if r > 0.15 else BLUE for r in dept['Rate']],
               height=0.55, edgecolor='white', linewidth=0.5)
for bar, (_, row) in zip(bars, dept.iterrows()):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{row['Rate']:.1%}  ({int(row['Attrited'])}/{int(row['Total'])})",
            va='center', fontsize=10, color=NAVY, fontweight='bold')
ax.set_xlabel('Attrition Rate (%)', color=GRAY)
ax.set_title('Attrition Rate by Department')
ax.set_xlim(0, 30)
ax.axvline(df['AttritionBinary'].mean()*100, color=AMBER,
           linestyle='--', linewidth=1.5, label=f"Avg {df['AttritionBinary'].mean():.1%}")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/02_attrition_by_dept.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 2: By department")


# ────────────────────────────────────────────────────────────
# CHART 3 — Overtime vs Attrition
# ────────────────────────────────────────────────────────────
ot = df.groupby(['OverTime','Attrition']).size().unstack(fill_value=0)
ot_pct = ot.div(ot.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(len(ot_pct))
w = 0.35
b1 = ax.bar(x - w/2, ot_pct['No'],  w, label='Active',   color=GREEN, edgecolor='white')
b2 = ax.bar(x + w/2, ot_pct['Yes'], w, label='Attrited', color=RED,   edgecolor='white')
for bar in [*b1, *b2]:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(ot_pct.index, fontsize=11)
ax.set_ylabel('% of Employees'); ax.set_xlabel('OverTime', color=GRAY)
ax.set_title('Attrition vs Overtime Status\n(Overtime employees leave at ~2× rate)')
ax.legend(); ax.set_ylim(0, 95)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/03_overtime_attrition.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 3: Overtime vs attrition")


# ────────────────────────────────────────────────────────────
# CHART 4 — Monthly Income Distribution
# ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
bins = np.linspace(df['MonthlyIncome'].min(), df['MonthlyIncome'].max(), 30)
ax.hist(attr_no['MonthlyIncome'],  bins=bins, alpha=0.7, color=BLUE,  label='Active',   edgecolor='white')
ax.hist(attr_yes['MonthlyIncome'], bins=bins, alpha=0.8, color=RED,   label='Attrited', edgecolor='white')
ax.axvline(attr_no['MonthlyIncome'].mean(),  color=BLUE,  linestyle='--', linewidth=1.5,
           label=f"Active avg ₹{attr_no['MonthlyIncome'].mean():,.0f}")
ax.axvline(attr_yes['MonthlyIncome'].mean(), color=RED,   linestyle='--', linewidth=1.5,
           label=f"Attrited avg ₹{attr_yes['MonthlyIncome'].mean():,.0f}")
ax.set_xlabel('Monthly Income (₹)', color=GRAY)
ax.set_ylabel('Number of Employees')
ax.set_title('Income Distribution — Attrited vs Active\n(Lower earners leave more)')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/04_income_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 4: Income distribution")


# ────────────────────────────────────────────────────────────
# CHART 5 — Job Satisfaction & Work-Life Balance Heatmap
# ────────────────────────────────────────────────────────────
pivot = df.groupby(['JobSatisfaction','WorkLifeBalance'])['AttritionBinary'].mean().unstack()
pivot.index = ['Low','Medium','High','Very High']
pivot.columns = ['Bad','Good','Better','Best']

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot * 100, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=0.5, linecolor='white', ax=ax,
            cbar_kws={'label': 'Attrition Rate (%)'})
ax.set_xlabel('Work-Life Balance', fontweight='bold')
ax.set_ylabel('Job Satisfaction', fontweight='bold')
ax.set_title('Attrition Rate Heatmap\nJob Satisfaction × Work-Life Balance (%)')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/05_satisfaction_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 5: Satisfaction heatmap")


# ────────────────────────────────────────────────────────────
# CHART 6 — Attrition by Tenure Band
# ────────────────────────────────────────────────────────────
ten = df.groupby('TenureBand', observed=True)['AttritionBinary'].agg(['mean','count']).reset_index()
ten.columns = ['Tenure','Rate','Count']

fig, ax = plt.subplots(figsize=(7, 4.5))
colors_t = [RED if r > 0.18 else BLUE for r in ten['Rate']]
bars = ax.bar(ten['Tenure'], ten['Rate']*100, color=colors_t,
              width=0.5, edgecolor='white', linewidth=0.5)
for bar, (_, row) in zip(bars, ten.iterrows()):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
            f"{row['Rate']:.1%}\n(n={int(row['Count'])})",
            ha='center', fontsize=9.5, fontweight='bold', color=NAVY)
ax.set_xlabel('Years at Company', color=GRAY)
ax.set_ylabel('Attrition Rate (%)')
ax.set_title('Attrition Rate by Tenure Band\n(New joiners 0-2 yrs are highest risk)')
ax.axhline(df['AttritionBinary'].mean()*100, color=AMBER,
           linestyle='--', linewidth=1.5, label=f"Avg {df['AttritionBinary'].mean():.1%}")
ax.legend(); ax.set_ylim(0, 38)
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/06_attrition_by_tenure.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 6: By tenure band")


# ────────────────────────────────────────────────────────────
# CHART 7 — Correlation Matrix (key numeric columns)
# ────────────────────────────────────────────────────────────
num_cols = ['AttritionBinary','Age','MonthlyIncome','YearsAtCompany',
            'JobSatisfaction','WorkLifeBalance','EnvironmentSatisfaction',
            'DistanceFromHome','NumCompaniesWorked','YearsSinceLastPromotion']
corr = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.5, linecolor='white', ax=ax,
            vmin=-0.5, vmax=0.5)
labels = ['Attrition','Age','Income','Tenure','Job Sat.','WLB',
          'Env Sat.','Distance','# Companies','Yrs Since Promo']
ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
ax.set_yticklabels(labels, rotation=0, fontsize=9)
ax.set_title('Correlation Matrix — Key Variables\n(Focus on Attrition row)')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/07_correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 7: Correlation matrix")


# ────────────────────────────────────────────────────────────
# CHART 8 — Top Risk Factors (Attrition Rate by Category)
# ────────────────────────────────────────────────────────────
risk_factors = {
    'OverTime = Yes':           (df['OverTime']=='Yes').mean() * 100,
    'Marital = Single':         (df['MaritalStatus']=='Single').mean() * 100,
    'Job Satisfaction 1-2':     (df['JobSatisfaction']<=2).mean() * 100,
    'Work-Life Balance 1-2':    (df['WorkLifeBalance']<=2).mean() * 100,
    'Tenure 0-2 yrs':           (df['YearsAtCompany']<=2).mean() * 100,
    'No Stock Options':         (df['StockOptionLevel']==0).mean() * 100,
    'Frequent Travel':          (df['BusinessTravel']=='Travel_Frequently').mean() * 100,
    'Env Satisfaction 1-2':     (df['EnvironmentSatisfaction']<=2).mean() * 100,
}
attr_by_factor = {
    'OverTime = Yes':         df[df['OverTime']=='Yes']['AttritionBinary'].mean()*100,
    'Marital = Single':       df[df['MaritalStatus']=='Single']['AttritionBinary'].mean()*100,
    'Job Satisfaction 1-2':   df[df['JobSatisfaction']<=2]['AttritionBinary'].mean()*100,
    'Work-Life Balance 1-2':  df[df['WorkLifeBalance']<=2]['AttritionBinary'].mean()*100,
    'Tenure 0-2 yrs':         df[df['YearsAtCompany']<=2]['AttritionBinary'].mean()*100,
    'No Stock Options':       df[df['StockOptionLevel']==0]['AttritionBinary'].mean()*100,
    'Frequent Travel':        df[df['BusinessTravel']=='Travel_Frequently']['AttritionBinary'].mean()*100,
    'Env Satisfaction 1-2':   df[df['EnvironmentSatisfaction']<=2]['AttritionBinary'].mean()*100,
}

factors = list(attr_by_factor.keys())
rates   = list(attr_by_factor.values())
avg_r   = df['AttritionBinary'].mean() * 100

sorted_pairs = sorted(zip(rates, factors))
rates_s, factors_s = zip(*sorted_pairs)

fig, ax = plt.subplots(figsize=(9, 6))
bar_colors = [RED if r > avg_r*1.2 else AMBER if r > avg_r else BLUE for r in rates_s]
bars = ax.barh(factors_s, rates_s, color=bar_colors, height=0.55, edgecolor='white')
ax.axvline(avg_r, color=NAVY, linestyle='--', linewidth=1.5, label=f'Overall avg {avg_r:.1f}%')
for bar in bars:
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
            f'{bar.get_width():.1f}%', va='center', fontsize=9.5, fontweight='bold')
ax.set_xlabel('Attrition Rate (%)'); ax.set_xlim(0, 45)
ax.set_title('Attrition Rate by Key Risk Factors\n(Red = highest risk bands)')
red_p   = mpatches.Patch(color=RED,   label='High risk (>1.2× avg)')
amber_p = mpatches.Patch(color=AMBER, label='Medium risk (>avg)')
blue_p  = mpatches.Patch(color=BLUE,  label='Below avg')
ax.legend(handles=[red_p, amber_p, blue_p], fontsize=9, loc='lower right')
plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/08_risk_factors.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Chart 8: Risk factors summary")

print(f"\n✅  All 8 charts saved to ./{CHARTS_DIR}/")
print("\n── Key Stats ─────────────────────────────────────────")
print(f"  Overall attrition rate : {df['AttritionBinary'].mean():.1%}")
print(f"  OT attrition rate      : {df[df['OverTime']=='Yes']['AttritionBinary'].mean():.1%}")
print(f"  No-OT attrition rate   : {df[df['OverTime']=='No']['AttritionBinary'].mean():.1%}")
print(f"  Avg income (active)    : ₹{attr_no['MonthlyIncome'].mean():,.0f}")
print(f"  Avg income (attrited)  : ₹{attr_yes['MonthlyIncome'].mean():,.0f}")
print(f"  Avg tenure (active)    : {attr_no['YearsAtCompany'].mean():.1f} yrs")
print(f"  Avg tenure (attrited)  : {attr_yes['YearsAtCompany'].mean():.1f} yrs")
