#!/usr/bin/env bash

clean_up() {
	if [[ ! -z $PID ]] && kill -0 $PID 2> /dev/null; then
		kill $PID
		wait $PID 2>/dev/null
	fi
}

# trap clean_up EXIT INT TERM

# Server is ready
touch /vagrant/server_ready

# wait $PID
