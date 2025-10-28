import pandas as pd
import numpy as np
import os
from typing import List, Dict, Tuple
import argparse

def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    Calculate statistical metrics for a list of values.
    
    Args:
        data: List of numerical values (durations/times)
    
    Returns:
        Dictionary containing statistical metrics
    """
    if not data:
        return {
            'count': 0,
            'min': 0,
            'max': 0,
            'mean': 0,
            'median': 0,
            'p90': 0,
            'p95': 0
        }
    
    data_array = np.array(data)
    
    return {
        'count': len(data),
        'min': np.min(data_array),
        'max': np.max(data_array),
        'mean': np.mean(data_array),
        'median': np.median(data_array),
        'p90': np.percentile(data_array, 90),
        'p95': np.percentile(data_array, 95)
    }

def read_csv_file(file_path: str) -> Tuple[List[float], str]:
    """
    Read CSV file and extract timing data.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        Tuple of (timing_data, file_identifier)
    """
    try:
        df = pd.read_csv(file_path)
        file_name = os.path.basename(file_path)
        
        # Try different column names for timing data
        timing_columns = ['HTTP Request Time', 'time', 'avg', 'latency', 'duration']
        timing_data = []
        
        for col in timing_columns:
            if col in df.columns:
                timing_data = df[col].dropna().tolist()
                break
        
        if not timing_data:
            print(f"Warning: No timing data found in {file_name}")
            print(f"Available columns: {list(df.columns)}")
        
        return timing_data, file_name
    
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return [], os.path.basename(file_path)

def extract_metrics_from_files(file_paths: List[str]) -> None:
    """
    Extract and display metrics from multiple CSV files.
    
    Args:
        file_paths: List of file paths to analyze
    """
    print("=" * 80)
    print("NETWORK PERFORMANCE METRICS EXTRACTION")
    print("=" * 80)
    print()
    
    all_results = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        timing_data, file_name = read_csv_file(file_path)
        
        if timing_data:
            stats = calculate_statistics(timing_data)
            all_results.append((file_name, stats))
            
            print(f"FILE: {file_name}")
            print("-" * 50)
            print(f"Number of packets/requests: {stats['count']:,}")
            print(f"Minimum duration (s):       {stats['min']:.6f}")
            print(f"Maximum duration (s):       {stats['max']:.6f}")
            print(f"Average duration (s):       {stats['mean']:.6f}")
            print(f"Median duration (s):        {stats['median']:.6f}")
            print(f"90th percentile (s):        {stats['p90']:.6f}")
            print(f"95th percentile (s):        {stats['p95']:.6f}")
            print()
        else:
            print(f"No data extracted from: {file_name}")
            print()
    
    # Summary comparison table
    if len(all_results) > 1:
        print("=" * 80)
        print("COMPARISON SUMMARY")
        print("=" * 80)
        print()
        
        # Create comparison table
        headers = ["File", "Packets", "Min (s)", "Max (s)", "Avg (s)", "Median (s)", "P90 (s)", "P95 (s)"]
        
        # Print header
        print(f"{'File':<25} {'Packets':<10} {'Min (s)':<12} {'Max (s)':<12} {'Avg (s)':<12} {'Median (s)':<12} {'P90 (s)':<12} {'P95 (s)':<12}")
        print("-" * 25 + " " + "-" * 10 + " " + "-" * 12 + " " + "-" * 12 + " " + "-" * 12 + " " + "-" * 12 + " " + "-" * 12 + " " + "-" * 12)
        
        for file_name, stats in all_results:
            print(f"{file_name:<25} {stats['count']:<10,} {stats['min']:<12.6f} {stats['max']:<12.6f} {stats['mean']:<12.6f} {stats['median']:<12.6f} {stats['p90']:<12.6f} {stats['p95']:<12.6f}")
        
        print()

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description='Extract network performance metrics from CSV files')
    parser.add_argument('files', nargs='*', help='CSV files to analyze')
    parser.add_argument('--preset', choices=['24h', 'phase0', 'stress'], 
                       help='Use predefined file sets')
    
    args = parser.parse_args()
    
    # Define preset file sets
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    presets = {
        '24h': [
            os.path.join(base_path, 'data', '24h', '24h-bh-rj.csv'),
            os.path.join(base_path, 'data', '24h', '24h-bh.csv'),
            os.path.join(base_path, 'data', '24h', '24h-ip.csv'),
            os.path.join(base_path, 'data', '24h', '24h-rj.csv')
        ],
        'phase0': [
            os.path.join(base_path, 'data', 'phase0', 'times_raw_ip.csv'),
            os.path.join(base_path, 'data', 'phase0', 'times_raw_polka.csv'),
            os.path.join(base_path, 'data', 'phase0', 'times_treated_ip.csv'),
            os.path.join(base_path, 'data', 'phase0', 'times_treated_polka.csv')
        ],
        'stress': [
            os.path.join(base_path, 'data', 'stress', 'stress-ip.csv'),
            os.path.join(base_path, 'data', 'stress', 'stress-polka1.csv'),
            os.path.join(base_path, 'data', 'stress', 'stress-polka2.csv'),
            os.path.join(base_path, 'data', 'stress', 'stress-polka3.csv')
        ]
    }
    
    # Determine which files to process
    if args.preset:
        file_paths = presets.get(args.preset, [])
        if not file_paths:
            print(f"Unknown preset: {args.preset}")
            return
    elif args.files:
        file_paths = args.files
    else:
        # Default: analyze the 24h files
        file_paths = presets['24h']
        print("No files specified. Using default 24h files.")
        print()
    
    extract_metrics_from_files(file_paths)

if __name__ == "__main__":
    main()