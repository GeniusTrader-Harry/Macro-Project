import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d

df = pd.read_csv('Taiwan_Tax_Revenue_pct_GDP.csv')

window_size = 5
moving_avg = uniform_filter1d(df['Tax Revenue/GDP (%)'].values, size=window_size, mode='nearest')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(df['Year'], df['Tax Revenue/GDP (%)'],
        linewidth=2, color='#2E86AB', alpha=0.7, label='Tax/GDP Ratio')
ax.plot(df['Year'], moving_avg,
        linewidth=3, color='#A23B72', linestyle='--',
        label=f'{window_size}-Year Moving Average', alpha=0.8)

ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Tax Revenue (% of GDP)', fontsize=14, fontweight='bold')
ax.set_title(f'Taiwan: Tax Revenue as Share of GDP ({df["Year"].iloc[0]}-{df["Year"].iloc[-1]})',
             fontsize=16, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(bottom=df['Tax Revenue/GDP (%)'].min() * 0.95, top=df['Tax Revenue/GDP (%)'].max() * 1.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))
ax.legend(fontsize=12, loc='upper left')

initial_val = df['Tax Revenue/GDP (%)'].iloc[0]
final_val = df['Tax Revenue/GDP (%)'].iloc[-1]
peak_val = df['Tax Revenue/GDP (%)'].max()
peak_year = df.loc[df['Tax Revenue/GDP (%)'].idxmax(), 'Year']
change = final_val - initial_val

textstr = 'Key Statistics:\n'
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
print(f"- Tax/GDP ratio: {initial_val:.1f}% ({df['Year'].iloc[0]}) → {final_val:.1f}% ({df['Year'].iloc[-1]})")
print(f"- Peak: {peak_val:.1f}% in {peak_year}")
print(f"- Overall change: {change:+.1f} percentage points")
