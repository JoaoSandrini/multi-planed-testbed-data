import subprocess
import csv

tshark_cmd = [
    "tshark",
    "-r", "C:/Users/joaop/Desktop/NERDS/VIX-MIA-Proj/captures/phase1/captures/24h-bh-rj.pcap",
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


    
