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


dfs() {
	wget -P $SCRIPT_DIR "$link""$1" 
	file=$1
	[ -z $file ] && file="/pages/index.html"
	echo $file >> $SCRIPT_DIR"/visited"
	check $href && echo "Visiting $file"
	for href in $(cat $(echo $file | awk -F "/" '{print $3}') | grep ">a<" | awk -F '"' '{print $2}'); do
		check $href && dfs $href
	done
	return 0
}

if [ -z $ 1]; then
	echo "Usage: ./bot.sh [ IP ADDRESS ]"
fi


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "" > $SCRIPT_DIR"/visited"
link="http://"$1":8000"
dfs
# clean
