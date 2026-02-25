import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# --- Taiwan gov spending ---
df_raw = pd.read_csv('Taiwan_Gov_Spending.csv')
taiwan = df_raw[df_raw['Country'] == 'Taiwan'].iloc[0]
year_cols = df_raw.columns[4:]
years = year_cols.astype(int)
values = taiwan[year_cols].astype(float) * 100
df_spend = pd.DataFrame({'Year': years, 'Gov_Spending_Pct': values}).reset_index(drop=True)

# --- Taiwan GDP per capita growth rate ---
gdp_raw = pd.read_csv('GDP per capita Database.csv', on_bad_lines='skip')
gdp_tw = gdp_raw[gdp_raw['Entity'] == 'Taiwan'][['Year', 'GDP per capita']].sort_values('Year').reset_index(drop=True)
gdp_tw['GDP_Growth'] = gdp_tw['GDP per capita'].pct_change() * 100

# --- Merge on Year, filter post-1960 ---
df = pd.merge(df_spend, gdp_tw[['Year', 'GDP_Growth']], on='Year').dropna()
df = df[df['Year'] > 1964].reset_index(drop=True)

x = df['Gov_Spending_Pct'].values
y = df['GDP_Growth'].values

# --- Regression ---
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
x_line = np.linspace(x.min(), x.max(), 200)
y_line = slope * x_line + intercept

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(x, y, color='#2E86AB', alpha=0.7, s=50, zorder=3, label='Annual observations')
ax.plot(x_line, y_line, color='#A23B72', linewidth=2, label=f'Line of best fit')

ax.set_xlabel('Government Consumption (% of GDP)', fontsize=13, fontweight='bold')
ax.set_ylabel('GDP per Capita Growth Rate (%)', fontsize=13, fontweight='bold')
ax.set_title('Taiwan: Government Spending vs. GDP per Capita Growth Rate',
             fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, linestyle='--')

# Regression stats box
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
textstr  = 'Regression Analysis:\n'
textstr += f'Slope: {slope:.3f}\n'
textstr += f'Intercept: {intercept:.3f}\n'
textstr += f'R²: {r_value**2:.3f}\n'
textstr += f'p-value: {p_value:.4f}\n'
textstr += f'Std Error: {std_err:.4f}\n'
textstr += f'n = {len(df)}'
ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right', bbox=props)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f'{v:.1f}%'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f'{v:.1f}%'))
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('Taiwan_Spending_vs_GDPGrowth_scatter.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'Taiwan_Spending_vs_GDPGrowth_scatter.png'")
print(f"Slope: {slope:.3f} | R²: {r_value**2:.3f} | p-value: {p_value:.4f}")
