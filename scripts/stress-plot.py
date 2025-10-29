import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

# Set seaborn style and color palette
# Seaborn style + larger default fonts for readability
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.35)
# Use the default seaborn palette to match histogram colors
colors = sns.color_palette("tab10")  # This gives: blue, orange, green, red, etc.

# Carregar os dados dos testes de stress
df_stress_ip = pd.read_csv('csv-data/stress-ip.csv')
df_stress_polka1 = pd.read_csv('csv-data/stress-polka-1.csv')
df_stress_polka2 = pd.read_csv('csv-data/stress-polka-2.csv')
df_stress_polka3 = pd.read_csv('csv-data/stress-polka-3.csv')

# Filtrar dados para apenas até 20 minutos (1200 segundos)
df_stress_ip = df_stress_ip[df_stress_ip['time'] <= 1200]
df_stress_polka1 = df_stress_polka1[df_stress_polka1['time'] <= 1200]
df_stress_polka2 = df_stress_polka2[df_stress_polka2['time'] <= 1200]
df_stress_polka3 = df_stress_polka3[df_stress_polka3['time'] <= 1200]

# Plotar os dados
plt.figure(figsize=(10, 6))
plt.plot(df_stress_ip['time']/60, df_stress_ip['avg'], label='IP: 17 Hops', linewidth=2, marker='o', markersize=3, color=colors[0])  # Blue
plt.plot(df_stress_polka1['time']/60, df_stress_polka1['avg'], label='PolKA 1: VIX-RIO-SAO-MIA', linewidth=2, marker='s', markersize=3, color=colors[1])  # Orange
plt.plot(df_stress_polka2['time']/60, df_stress_polka2['avg'], label='PolKA 2: VIX-BHZ-SAO-MIA', linewidth=2, marker='^', markersize=3, color=colors[2])  # Green
plt.plot(df_stress_polka3['time']/60, df_stress_polka3['avg'], label='PolKA 3: VIX-BHZ-RIO-SAO-MIA', linewidth=2, marker='d', markersize=3, color=colors[3])  # Red



# Adicionar rótulos e título
plt.xlabel('Time (minutes)', fontsize=20)
plt.ylabel('Average Throughput (Gb/s)', fontsize=20)
plt.title('Average Throughput Comparison: IP vs PolKA 1, 2, 3', fontsize=24, fontweight='bold')

plt.xticks(range(0, 21, 2))  # De 0 a 20 minutos, a cada 2 minutos

# Ajustar limites dos eixos para ocupar todo o espaço do gráfico
#plt.xlim(0, 20)  # Exatamente de 0 a 20 minutos
#plt.ylim(0, None)  # Começar do zero, deixar matplotlib determinar o máximo
plt.yscale('log')

# Make y-tick values more readable and increase tick label font sizes
from matplotlib.ticker import FuncFormatter

def format_throughput(x, pos):
    """Format throughput values for better readability"""
    if x >= 1:
        return f'{x:.1f}'
    elif x >= 0.1:
        return f'{x:.2f}'
    else:
        return f'{x:.3f}'

# Use the current axis object to set tick properties
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(format_throughput))
# Set specific y-tick locations for better readability
ax.set_yticks([0.01, 0.1, 1, 10, 100])

# Configure minor ticks: for x use AutoMinorLocator, for log-y use LogLocator if available
try:
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
except Exception:
    ax.minorticks_on()

try:
    # Place minor ticks at 2-9 per decade for log scale
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=range(1, 10)))
except Exception:
    ax.minorticks_on()

# Make major tick labels larger and more visible
ax.tick_params(axis='both', which='major', labelsize=14, length=8, width=1.6, direction='in')
# Make minor ticks slightly smaller but still visible (they typically don't have labels)
ax.tick_params(axis='both', which='minor', labelsize=12, length=6, width=1.2, color='gray', direction='in')

# Increase legend font size for consistency
plt.legend(fontsize=18, loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('result-plots/stress.png', dpi=300, bbox_inches='tight')  # Save the figure