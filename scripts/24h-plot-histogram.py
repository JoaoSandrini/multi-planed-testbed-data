import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
import csv
import os
from matplotlib.patches import Patch

# File paths
SET_FILES = {
    "IP: 17 Hops": "./csv-data/24h-ip.csv",
    "PolKA 1: VIT-RIO-SAO-MIA": "./csv-data/24h-polka-1.csv",
    "PolKA 2: VIT-BHZ-SAO-MIA": "./csv-data/24h-polka-2.csv",
    "PolKA 3: VIT-BHZ-RIO-SAO-MIA": "./csv-data/24h-polka-3.csv",
}
OUTPUT_FILE = "result-plots/24h-histogram.png"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Function to read all values from the first column of a CSV
def read_times_from_csv(filepath):
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # skip header
        times = [float(row[2])*1000 for row in reader if row[2] != '']
    return times

# Read all datasets
all_data = []
for set_name, filepath in SET_FILES.items():
    times = read_times_from_csv(filepath)
    all_data.extend([(t, set_name) for t in times])

# Convert to DataFrame
df = pd.DataFrame(all_data, columns=["Time", "Path"])

# Freedman–Diaconis rule for bin size
def freedman_diaconis_bins(data):
    q25, q75 = np.percentile(data, [25, 75])
    iqr = q75 - q25
    n = len(data)
    bin_width = 2 * iqr / (n ** (1/3))
    if bin_width <= 0:
        return 100  # fallback
    return max(10, int((max(data) - min(data)) / bin_width))

bin_count = freedman_diaconis_bins(df["Time"])

# Plot

sns.set(style="whitegrid")
# Increase overall font sizes for tick labels, axes labels and titles
# font_scale scales Seaborn's font sizes (works well with matplotlib)
sns.set_context("notebook")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Add main title
fig.suptitle("HTTP Response Time Density Curve per Path", fontsize=24, fontweight='bold')

# Define the subplot positions for each dataset
# Top row: PolKA 1, PolKA 2
# Bottom row: PolKA 3, IP
subplot_order = ["PolKA 1: VIT-RIO-SAO-MIA", "PolKA 2: VIT-BHZ-SAO-MIA", "PolKA 3: VIT-BHZ-RIO-SAO-MIA", "IP: 17 Hops"]
positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Get the color palette that seaborn would use
colors = sns.color_palette("tab10", n_colors=len(SET_FILES))
color_map = {list(SET_FILES.keys())[i]: colors[i] for i in range(len(SET_FILES))}

for idx, (set_name, pos) in enumerate(zip(subplot_order, positions)):
    row, col = pos
    ax = axes[row, col]
    
    # Filter data for this specific dataset
    subset_data = df[df["Path"] == set_name]
    # Remove non-positive values antes de usar escala log
    subset_data = subset_data[subset_data["Time"] > 0]
    if subset_data.empty:
        ax.set_title(set_name + " (no positive values)", fontsize=20, fontweight='bold')
        ax.set_xlabel("" if row == 0 else "Response Time (ms)")
        ax.set_ylabel("" if col != 0 else "Probability Density")
        continue
    
    # Create histogram for this subset
    sns.histplot(
        data=subset_data,
        x="Time",
        element="step",
        stat="density",
        bins=bin_count,
        fill=True,
        alpha=0.7,
        color=color_map[set_name],
        ax=ax
    )
    
    # Set title to just the path name
    ax.set_title(set_name, fontsize=20, fontweight='bold')
    
    # Only add x-axis label for bottom row
    if row == 1:
        ax.set_xlabel("Response Time (ms)", fontsize=20)
    else:
        ax.set_xlabel("")
    
    # Only add y-axis label for left column
    if col == 0:
        ax.set_ylabel("Probability Density", fontsize=20)
    else:
        ax.set_ylabel("")
    
    ax.set_yscale('log')
    ax.set_xscale('log')

    # Make major tick labels bigger and consistent across all subplots
    ax.tick_params(axis='x', which='major', labelsize=16)
    ax.tick_params(axis='y', which='major', labelsize=16)

    # Minor ticks (kept smaller but visible) - keep a consistent labelsize if shown
    ax.tick_params(axis='x', which='minor', length=4, color='gray', labelsize=16)
    ax.tick_params(axis='y', which='minor', length=4, color='gray', labelsize=16)
     
    # Optional: enable minor grid for better readability
    ax.grid(True, which='minor', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

plt.tight_layout(rect=(0, 0.03, 1, 0.97))
# Save plot
plt.savefig(OUTPUT_FILE, dpi=300)
plt.close()
