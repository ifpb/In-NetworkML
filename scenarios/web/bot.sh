#!/bin/bash
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
	echo "-----SOS-----" >> snapshots
	echo "Visiting $link/$file" >> snapshots
	echo "TIMESTAMP=$(date +%s%3N)" >> snapshots
	curl -w "
Time Details:
-------------
Name Lookup:    %{time_namelookup}s
Connect:        %{time_connect}s
Pre-transfer:   %{time_pretransfer}s
Start-transfer: %{time_starttransfer}s
Total:          %{time_total}s

Size Details:
-------------
Download:       %{size_download} bytes
Header Size:    %{size_header} bytes

HTTP Code:      %{http_code}
	" -o $file "$link/$1" >> snapshots
	echo "-----EOS------
"	>> snapshots
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

echo "" > visited
echo "" > snapshots
link="http://"$1
dfs
clean
