import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# === FILE PATHS ===
CSV = 'data/phase1/route-swap.csv'

# Ensure output directory exists
os.makedirs('result-plots/phase1', exist_ok=True)

# === READ CSV FILES ===
def read_times_from_csv(filepath):
    times = []
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            try:
                times.append(float(row[1])*1000)
            except ValueError:
                continue
    return np.array(times)

# Read all datasets
times = read_times_from_csv(CSV)

# Align lengths
x = np.arange(1, len(times) + 1)

# Seaborn style
sns.set(style="whitegrid", palette="Set2", font_scale=1.1)

# Plot each scenario in a separate image
scenarios = [
    ('Route Swap', times, 'blue', 'result-plots/phase1/route-swap.png'),
]

for label, times, color, filename in scenarios:
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=x, y=times, color=color, linewidth=1.5)
    plt.title(f'HTTP Request Times - {label}', fontsize=20, fontweight='bold')
    plt.xlabel('Request Number', fontsize=14)
    plt.ylabel('HTTP Request Time (ms)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()