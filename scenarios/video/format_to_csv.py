#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-i', required=True, help='input file')
parser.add_argument('-o', required=True, help='output file')
args = parser.parse_args()

# Define the input file path
input_file_path = args.i

# Output CSV file
output_file = args.o

# Open the input file and read the data
with open(input_file_path, 'r') as file:
    log_data = file.readlines()

# Define the header for the CSV
header = ["frame", "fps", "stream_0_0_q", "bitrate", "total_size", "out_time_us", "out_time_ms", "out_time", "dup_frames", "drop_frames", "speed"]

# Write the header to the output CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # Process each line from the log file
    for line in log_data:
        # Strip any leading/trailing whitespace or newlines
        line = line.strip()

        # Split the line by commas
        entries = line.split(',')

        # Initialize an empty list to hold the values for the current row
        row = []

        # Process each key-value pair in the entries
        for entry in entries:
            # Split by '=' and extract the value
            key, value = entry.split('=')
            row.append(value.strip())

        # Write the row to the CSV file
        writer.writerow(row)

# print(f"Log data has been formatted and saved to '{output_file}'.")
