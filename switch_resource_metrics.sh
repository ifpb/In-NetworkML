#!/usr/bin/env bash

OUTPUT_DIR="${OUTPUT_DIR:-/vagrant/metrics}"
FILE_PATH="${OUTPUT_DIR}/system_metrics.csv"

STOPPED=false

trap "STOPPED=true" TERM INT

mkdir -p $OUTPUT_DIR

echo "timestamp,cpu_total,cpu_user,cpu_sys,cpu_idle,mem_total,mem_free,mem_used,mem_cache,load_avg" > $FILE_PATH

while ! $STOPPED; do
	TIMESTAMP=$(date +"%s%3N")
	top -bn1 | awk -v ts="$TIMESTAMP" '
	BEGIN {OFS=","}
	/load average:/ {
		load = $12
		gsub(/,/, "", load)
	}
	/^%Cpu\(s\):/ {
		user = $2
		sys = $4
		idle = $8
		total = 100-idle
	}
	/^KiB Mem :/ {
		total_mem = $4
		free = $6
		used = $8
		cache = $10
	}

	END {
		print ts,total,user,sys,idle,total_mem,free,used,cache,load
	}' >> "$FILE_PATH"
done
