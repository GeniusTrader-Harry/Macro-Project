import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d

# --- Taiwan data ---
df = pd.read_csv('Taiwan_Tax_Revenue_pct_GDP.csv')

# --- OECD data ---
oecd_raw = pd.read_csv('OECD_Tax_Revenue_DataSet.csv')
df_oecd = oecd_raw[['TIME_PERIOD', 'OBS_VALUE']].dropna().sort_values('TIME_PERIOD').reset_index(drop=True)
df_oecd.columns = ['Year', 'Tax_GDP']

window_size = 5
moving_avg = uniform_filter1d(df['Tax Revenue/GDP (%)'].values, size=window_size, mode='nearest')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(df['Year'], df['Tax Revenue/GDP (%)'],
        linewidth=2, color='#2E86AB', alpha=0.7, label='Taiwan Tax/GDP Ratio')
ax.plot(df['Year'], moving_avg,
        linewidth=3, color='#A23B72', linestyle='--',
        label=f'Taiwan {window_size}-Year Moving Avg', alpha=0.8)
ax.plot(df_oecd['Year'], df_oecd['Tax_GDP'],
        linewidth=2, color='#E07B39', alpha=0.8, label='OECD Average')

ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Tax Revenue (% of GDP)', fontsize=14, fontweight='bold')
ax.set_title('Taiwan: Tax Revenue as a Share of GDP',
             fontsize=16, fontweight='bold', pad=20)

all_vals = pd.concat([df['Tax Revenue/GDP (%)'], df_oecd['Tax_GDP']])
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(bottom=all_vals.min() * 0.95, top=all_vals.max() * 1.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))
ax.legend(fontsize=12, loc='upper left')

initial_val = df['Tax Revenue/GDP (%)'].iloc[0]
final_val = df['Tax Revenue/GDP (%)'].iloc[-1]
peak_val = df['Tax Revenue/GDP (%)'].max()
peak_year = df.loc[df['Tax Revenue/GDP (%)'].idxmax(), 'Year']
change = final_val - initial_val

textstr = 'Taiwan Key Statistics:\n'
textstr += f'Initial ({df["Year"].iloc[0]}): {initial_val:.1f}%\n'
textstr += f'Final ({df["Year"].iloc[-1]}): {final_val:.1f}%\n'
textstr += f'Peak: {peak_val:.1f}% ({peak_year})\n'
textstr += f'Overall Change: {change:+.1f} pp'

ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('Taiwan_Tax_GDP_trend.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'Taiwan_Tax_GDP_trend.png'")
print(f"- Taiwan tax/GDP ratio: {initial_val:.1f}% ({df['Year'].iloc[0]}) → {final_val:.1f}% ({df['Year'].iloc[-1]})")
print(f"- Peak: {peak_val:.1f}% in {peak_year}")
print(f"- Overall change: {change:+.1f} percentage points")
