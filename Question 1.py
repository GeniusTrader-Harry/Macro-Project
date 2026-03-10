import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d
from matplotlib.ticker import FixedLocator

# Read the CSV file and filter for Taiwan from 1900 onwards
df_full = pd.read_csv('GDP per capita Database.csv')
df_full = df_full[(df_full['Entity'] == 'Taiwan') & (df_full['Year'] >= 1900)].reset_index(drop=True)

# Also create a 1950+ subset
df_1950 = df_full[df_full['Year'] >= 1950].reset_index(drop=True)

window_size = 5
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

PHASES = [
    ('Colonial\nModernisation', 1895, 1937, '#FFDDB3', '~2% p.a.'),
    ('Recovery &\nLand Reform',  1945, 1962, '#B3FFD1', '~9% p.a.'),
    ('Export-Led\nGrowth',       1962, 1980, '#B3D9FF', '~10% p.a.'),
    ('High-Tech\nTransition',    1980, 2000, '#E8B3FF', '~6.5% p.a.'),
    ('Innovation\nEconomy',      2000, 2022, '#FFFBB3', '~3% p.a.'),
]


def add_phase_bands(ax, df):
    x_min = df['Year'].min()
    x_max = df['Year'].max()
    trans = ax.get_xaxis_transform()
    LABEL_Y = 0.97  # fixed y for all labels (axes fraction)

    for i, (name, start, end, color, growth) in enumerate(PHASES):
        band_start = max(start, x_min)
        band_end = min(end, x_max)
        if band_start >= band_end:
            continue

        ax.axvspan(band_start, band_end, alpha=0.18, color=color, zorder=0)

        if i == 0:
            label_x, ha = band_end - 1, 'right'
        else:
            label_x, ha = (band_start + band_end) / 2, 'center'

        ax.text(label_x, LABEL_Y, f"{name}\n{growth}", transform=trans,
                ha=ha, va='top', fontsize=8.5, fontweight='bold',
                color='#222222', multialignment=ha, linespacing=1.4)

    # WWII gap label (only if the gap is visible in this chart)
    wwii_start = max(1937, x_min)
    wwii_end   = min(1945, x_max)
    if wwii_end > wwii_start:
        mid_wwii = (wwii_start + wwii_end) / 2
        ax.text(mid_wwii, LABEL_Y, 'WWII', transform=trans,
                ha='center', va='top', fontsize=8.5, fontweight='bold',
                color='#222222', multialignment='center')


def plot_log_graph(df, filename, title_suffix):
    """Plot a log-scale GDP per capita graph for the given dataframe."""
    moving_avg = uniform_filter1d(df['GDP per capita'].values, size=window_size, mode='nearest')

    fig, ax = plt.subplots(figsize=(14, 8))

    add_phase_bands(ax, df)

    ax.plot(df['Year'], df['GDP per capita'],
            linewidth=2, color='#2E86AB', alpha=0.7, label='GDP per Capita')
    ax.plot(df['Year'], moving_avg,
            linewidth=3, color='#A23B72', linestyle='--',
            label=f'{window_size}-Year Moving Average', alpha=0.8)

    ax.set_yscale('log')

    # Set explicit y-axis ticks for readability
    tick_values = [1000, 2000, 5000, 10000, 20000, 50000]
    ax.yaxis.set_major_locator(FixedLocator(tick_values))
    ax.yaxis.set_minor_locator(FixedLocator([]))
    ax.set_ylim(800, 80000)

    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Real GDP per Capita (2017 US$, log scale)', fontsize=14, fontweight='bold')
    ax.set_title(f'Taiwan: Long-Run Trend of GDP per Capita — Log Scale ({title_suffix})',
                 fontsize=16, fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.legend(fontsize=12, loc='upper left')

    # Growth statistics
    initial_gdp = df['GDP per capita'].iloc[0]
    final_gdp = df['GDP per capita'].iloc[-1]
    total_growth = ((final_gdp - initial_gdp) / initial_gdp) * 100
    years = df['Year'].iloc[-1] - df['Year'].iloc[0]
    cagr = ((final_gdp / initial_gdp) ** (1/years) - 1) * 100

    textstr = f'Growth Statistics:\n'
    textstr += f'Initial GDP per capita ({df["Year"].iloc[0]}): ${initial_gdp:,.0f}\n'
    textstr += f'Final GDP per capita ({df["Year"].iloc[-1]}): ${final_gdp:,.0f}\n'
    textstr += f'Total Growth: {total_growth:.1f}%\n'
    textstr += f'CAGR: {cagr:.2f}%'

    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

    print(f"Graph saved as '{filename}'")
    print(f"- GDP per capita grew from ${initial_gdp:,.0f} ({df['Year'].iloc[0]}) to ${final_gdp:,.0f} ({df['Year'].iloc[-1]})")
    print(f"- Total Growth: {total_growth:.1f}% | CAGR: {cagr:.2f}%\n")


# --- Log-scale: 1900 onwards ---
plot_log_graph(df_full, 'Taiwan_GDP_per_capita_trend_log.png',
               f'{df_full["Year"].iloc[0]}-{df_full["Year"].iloc[-1]}')

# --- Log-scale: 1950 onwards ---
plot_log_graph(df_1950, 'Taiwan_GDP_per_capita_trend_log_1950.png',
               f'{df_1950["Year"].iloc[0]}-{df_1950["Year"].iloc[-1]}')
