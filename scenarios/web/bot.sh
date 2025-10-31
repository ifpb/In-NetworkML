#!/bin/bash

PCAP_DIR=$2
METRICS_FILE="$PCAP_DIR""/http_metrics.csv"

clean() {
	rm $(ls -l | grep .html | awk '{print $9}')
}

debug() {
	echo "debug" $1 $2 $3 $4 $5
}

check() {
	[ -z $(cat visited | grep "$1" | head -n1 ) ] && return 0
	return 1
}

get_file() {
	file=$1
	[ -z $file ] && file="index.html"
	echo -n "$(date +%s%3N)," >> $METRICS_FILE
	curl -w "%{time_namelookup},%{time_connect},%{time_pretransfer},%{time_starttransfer},%{time_total},%{size_download},%{size_header},%{http_code}" -o $file "$link/$1" >> $METRICS_FILE
	echo "" >> $METRICS_FILE
}

dfs() {
	file=$1
	[ -z $file ] && file="index.html"
	echo $file >> visited
	get_file $1
	# check $href && echo "Visiting $file"
	for href in $(cat $file | grep ">a<" | awk -F '"' '{print $2}'); do
		check $href && dfs $href
	done
	return 0
}

if [ -z $1 ]; then
	echo "Usage: ./bot.sh [ IP ADDRESS ]"
fi


echo "timestamp,time_namelookup,time_connect,time_pretransfer,time_starttransfer,time_total,size_download,size_header,http_code" > $METRICS_FILE
echo "" > visited
link="http://"$1
dfs
clean
