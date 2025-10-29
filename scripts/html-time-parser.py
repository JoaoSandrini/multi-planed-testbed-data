import subprocess
import csv
import os
import glob


script_dir = os.path.dirname(os.path.abspath(__file__))

search_dirs = [
    os.path.join(script_dir, 'packet-captures'),
    os.path.join(script_dir, '..', 'packet-captures'),
    os.path.join(script_dir, '..', '..', 'packet-captures'),
]

found_files = []
for d in search_dirs:
    if os.path.isdir(d):
        for pattern in ('*.pcap', '*.pcapng', '*.cap', '*.pcap.gz'):
            found_files.extend(glob.glob(os.path.join(d, pattern)))

# If none found in the common locations, search recursively from script_dir
if not found_files:
    for pattern in ('*.pcap', '*.pcapng', '*.cap', '*.pcap.gz'):
        found_files.extend(glob.glob(os.path.join(script_dir, '**', pattern), recursive=True))

if not found_files:
    raise SystemExit("No packet capture file found in any 'packet-captures' directory under the script path.")

# pick the most recently modified capture file
capture_file = max(found_files, key=os.path.getmtime)
print(f"Using capture file: {capture_file}")

tshark_cmd = [
    "tshark",
    "-r", capture_file,
    "-Y", "http.time",
    "-T", "fields",
    "-e", "frame.time_utc",
    "-e", "http.time"
]

result = subprocess.run(tshark_cmd, capture_output=True, text=True)
lines = result.stdout.strip().split('\n')

with open('data/24h/24h-bh-rj.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Request Number', 'UTC Arrival Time', 'HTTP Request Time'])
    for idx, line in enumerate(lines):
        if line.strip():  # skip empty lines
            fields = line.split('\t')  # tshark separates fields with tabs
            if len(fields) >= 2:
                utc_time = fields[0]
                http_time = fields[1]
                csv_writer.writerow([idx + 1, utc_time, http_time])
            elif len(fields) == 1 and fields[0]:
                # In case there's only one field, it might be just the frame time
                csv_writer.writerow([idx + 1, fields[0], ''])



