import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d

# Read the CSV file
df = pd.read_csv('Taiwan GDP per capita.csv')

# Convert observation_date to datetime
df['observation_date'] = pd.to_datetime(df['observation_date'])

# Extract year for x-axis
df['year'] = df['observation_date'].dt.year

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Plot the actual GDP per capita
ax.plot(df['year'], df['RGDPCHTWA625NUPN'],
        linewidth=2, color='#2E86AB', alpha=0.7, label='GDP per Capita')

# Add a moving average trend line to show long-term trend (5-year moving average)
window_size = 5
moving_avg = uniform_filter1d(df['RGDPCHTWA625NUPN'], size=window_size, mode='nearest')
ax.plot(df['year'], moving_avg,
        linewidth=3, color='#A23B72', linestyle='--',
        label=f'{window_size}-Year Moving Average', alpha=0.8)

# Formatting
ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Real GDP per Capita (2017 US$)', fontsize=14, fontweight='bold')
ax.set_title('Taiwan: Long-Run Trend of GDP per Capita (1951-2010)',
             fontsize=16, fontweight='bold', pad=20)

# Add grid for better readability
ax.grid(True, alpha=0.3, linestyle='--')

# Format y-axis to show values in thousands with comma separator
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Add legend
ax.legend(fontsize=12, loc='upper left')

# Add some key statistics as text
initial_gdp = df['RGDPCHTWA625NUPN'].iloc[0]
final_gdp = df['RGDPCHTWA625NUPN'].iloc[-1]
total_growth = ((final_gdp - initial_gdp) / initial_gdp) * 100
years = df['year'].iloc[-1] - df['year'].iloc[0]
cagr = ((final_gdp / initial_gdp) ** (1/years) - 1) * 100

# Add text box with key statistics (positioned in bottom right)
textstr = f'Growth Statistics:\n'
textstr += f'Initial GDP per capita ({df["year"].iloc[0]}): ${initial_gdp:,.0f}\n'
textstr += f'Final GDP per capita ({df["year"].iloc[-1]}): ${final_gdp:,.0f}\n'
textstr += f'Total Growth: {total_growth:.1f}%\n'
textstr += f'CAGR: {cagr:.2f}%'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

# Tight layout
plt.tight_layout()

# Save the figure
plt.savefig('Taiwan_GDP_per_capita_trend.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()

# --- Log-scale version ---
fig2, ax2 = plt.subplots(figsize=(14, 8))

ax2.plot(df['year'], df['RGDPCHTWA625NUPN'],
         linewidth=2, color='#2E86AB', alpha=0.7, label='GDP per Capita')
ax2.plot(df['year'], moving_avg,
         linewidth=3, color='#A23B72', linestyle='--',
         label=f'{window_size}-Year Moving Average', alpha=0.8)

ax2.set_yscale('log')

# Set explicit y-axis ticks for readability
from matplotlib.ticker import FixedLocator
tick_values = [1000, 2000, 5000, 10000, 20000, 50000]
ax2.yaxis.set_major_locator(FixedLocator(tick_values))
ax2.yaxis.set_minor_locator(FixedLocator([]))
ax2.set_ylim(800, 50000)

ax2.set_xlabel('Year', fontsize=14, fontweight='bold')
ax2.set_ylabel('Real GDP per Capita (2017 US$, log scale)', fontsize=14, fontweight='bold')
ax2.set_title('Taiwan: Long-Run Trend of GDP per Capita — Log Scale (1951-2010)',
              fontsize=16, fontweight='bold', pad=20)

ax2.grid(True, alpha=0.3, linestyle='--', which='both')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax2.legend(fontsize=12, loc='upper left')

ax2.text(0.98, 0.02, textstr, transform=ax2.transAxes, fontsize=11,
         verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('Taiwan_GDP_per_capita_trend_log.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'Taiwan_GDP_per_capita_trend.png'")
print("Log-scale graph saved as 'Taiwan_GDP_per_capita_trend_log.png'")
print(f"\nKey Insights:")
print(f"- Taiwan's GDP per capita grew from ${initial_gdp:,.0f} in {df['year'].iloc[0]} to ${final_gdp:,.0f} in {df['year'].iloc[-1]}")
print(f"- This represents a {total_growth:.1f}% total growth over {years} years")
print(f"- Compound Annual Growth Rate (CAGR): {cagr:.2f}%")
