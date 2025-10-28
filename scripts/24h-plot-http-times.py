import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import os
from datetime import datetime, timedelta

# File paths
SET_FILES = {
    "PolKA 1: VIT-RIO-SAO-MIA": "data/24h/24h-rj.csv",
    "PolKA 2: VIT-BHZ-SAO-MIA": "data/24h/24h-bh.csv",
    "PolKA 3: VIT-BHZ-RIO-SAO-MIA": "data/24h/24h-bh-rj.csv",
    "IP: 17 Hops": "data/24h/24h-ip.csv",
}
OUTPUT_FILE_REQ = "result-plots/phase1/http-times-over-time-24h.png"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE_REQ), exist_ok=True)

# Read CSV times and timestamps
def read_times_and_timestamps_from_csv(filepath):
    timestamps = []
    http_times = []
    
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        
        for row in reader:
            if len(row) >= 3 and row[2] != '':  # Check if HTTP time exists
                try:
                    # Parse the timestamp format: "Jun 11, 2025 18:07:49.728608000 UTC"
                    timestamp_str = row[1].strip('"').replace(' UTC', '')
                    
                    # Handle nanoseconds - Python's strptime only handles microseconds (6 digits)
                    # So we need to truncate the nanoseconds to microseconds
                    if '.' in timestamp_str:
                        date_part, fraction_part = timestamp_str.split('.')
                        # Truncate to 6 digits (microseconds) and pad if necessary
                        fraction_part = fraction_part[:6].ljust(6, '0')
                        timestamp_str = f"{date_part}.{fraction_part}"
                    
                    timestamp = datetime.strptime(timestamp_str, "%b %d, %Y %H:%M:%S.%f")
                    timestamps.append(timestamp)
                    http_times.append(float(row[2]) * 1000)  # Convert to milliseconds
                except (ValueError, IndexError) as e:
                    print(f"Error parsing row: {row}, error: {e}")
                    continue
    
    return timestamps, http_times

# Define consistent color palette
colors = ['#ff7f0e', '#2ca02c', '#d62728', '#1f77b4']  # Reordered to keep IP blue in bottom-right
color_dict = dict(zip(SET_FILES.keys(), colors))

# Setup 2x2 subplot grid
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.flatten()

# Plot each dataset
for i, (label, filepath) in enumerate(SET_FILES.items()):
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} not found, skipping {label}")
        continue
        1
    timestamps, http_times = read_times_and_timestamps_from_csv(filepath)
    if not timestamps:
        print(f"Warning: No data found in {filepath}, skipping {label}")
        continue
        
    # Convert timestamps to hours of the day (0-24)
    hours_of_day = []
    sorted_http_times = []
    
    # Create pairs of (hour_of_day, http_time) and sort by hour
    time_pairs = [(dt.hour + dt.minute/60 + dt.second/3600 + dt.microsecond/3600000000, ht) 
                  for dt, ht in zip(timestamps, http_times)]
    time_pairs.sort(key=lambda x: x[0])  # Sort by hour of day
    
    hours_of_day = [pair[0] for pair in time_pairs]
    sorted_http_times = [pair[1] for pair in time_pairs]
    
    ax = axes[i]
    ax.plot(hours_of_day, sorted_http_times, color=color_dict[label], alpha=0.7, linewidth=0.8)
    ax.set_title(label, fontsize=14, fontweight='bold')
    
    if i >= 2:  # Bottom row
        ax.set_xlabel("Time (HH:MM)", fontsize=14)
    else:
        ax.set_xlabel("")  # Clear label
    ax.set_ylabel("Response Time (ms)" if i % 2 == 0 else "", fontsize=14)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    ax.set_yticks(range(0, 1300, 200))
    ax.set_yticklabels([f"{int(y)}" for y in ax.get_yticks()], fontsize=14)
    ax.set_ylim(0, 1200)  # Set y-limit
    ax.set_xlim(0, 24)  # 24-hour period
    # Set x-axis ticks every 4 hours
    ax.set_xticks(range(0, 25, 4))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 4)], fontsize=14)

# Remove unused axes if any
for j in range(len(SET_FILES), len(axes)):
    fig.delaxes(axes[j])

plt.suptitle("HTTP Response Time Over 24-Hour Period", fontsize=20, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.97])  # Adjust rect to make room for suptitle
plt.savefig(OUTPUT_FILE_REQ, dpi=300)
plt.close()

print(f"Plot saved to: {OUTPUT_FILE_REQ}")
