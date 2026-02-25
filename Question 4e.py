import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

# --- Taiwan GDP per capita growth rate ---
gdp_raw = pd.read_csv('GDP per capita Database.csv', on_bad_lines='skip')
gdp_tw = gdp_raw[gdp_raw['Entity'] == 'Taiwan'][['Year', 'GDP per capita']].sort_values('Year').reset_index(drop=True)
gdp_tw['GDP_Growth'] = gdp_tw['GDP per capita'].pct_change() * 100
gdp_tw = gdp_tw.dropna()

window_size = 5
moving_avg = uniform_filter1d(gdp_tw['GDP_Growth'].values, size=window_size, mode='nearest')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(gdp_tw['Year'], gdp_tw['GDP_Growth'],
        linewidth=2, color='#2E86AB', alpha=0.7, label='GDP per Capita Growth Rate')
ax.plot(gdp_tw['Year'], moving_avg,
        linewidth=3, color='#A23B72', linestyle='--',
        label=f'{window_size}-Year Moving Average', alpha=0.8)
ax.axhline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.4)

ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('GDP per Capita Growth Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('Taiwan: GDP per Capita Growth Rate Over Time',
             fontsize=16, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(bottom=gdp_tw['GDP_Growth'].min() * 1.2, top=gdp_tw['GDP_Growth'].max() * 1.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))
ax.legend(fontsize=12, loc='upper right')

# Key statistics
mean_growth = gdp_tw['GDP_Growth'].mean()
peak_val = gdp_tw['GDP_Growth'].max()
peak_year = gdp_tw.loc[gdp_tw['GDP_Growth'].idxmax(), 'Year']
trough_val = gdp_tw['GDP_Growth'].min()
trough_year = gdp_tw.loc[gdp_tw['GDP_Growth'].idxmin(), 'Year']

textstr  = 'Key Statistics:\n'
textstr += f'Mean Growth: {mean_growth:.1f}%\n'
textstr += f'Peak: {peak_val:.1f}% ({peak_year})\n'
textstr += f'Trough: {trough_val:.1f}% ({trough_year})'

ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='left', bbox=props)

plt.tight_layout()
plt.savefig('Taiwan_GDP_Growth_Rate.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'Taiwan_GDP_Growth_Rate.png'")
print(f"- Mean growth rate: {mean_growth:.1f}%")
print(f"- Peak: {peak_val:.1f}% in {peak_year}")
print(f"- Trough: {trough_val:.1f}% in {trough_year}")
