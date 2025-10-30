#!/usr/bin/env bash

# Test scenario duration in seconds, default = 60s
DURATION="${DURATION:-60}"
CAP_FILE="${CAP_FILE:-web_$(date +%s).pcap}"
PCAP_DIR="${PCAP_DIR:-/vagrant/pcap}"

CAP_FILE_PATH="${PCAP_DIR}/${CAP_FILE}"

SERVER_IP="192.168.56.102"
INTERFACE="eth1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_client() {
  while true; do
    ./bot.sh $SERVER_IP &
    echo $! > /tmp/bot.pid
    wait $(cat /tmp/bot.pid)
  done
}

mkdir -p $PCAP_DIR >/dev/null 2>&1
tcpdump -i $INTERFACE -w ${CAP_FILE_PATH} >/dev/null 2>&1 &
TCPDUMP_PID=$!

run_client &
CLIENT_PID=$!

clean_up() {
  BOT_PID=$(cat /tmp/bot.pid)
  if [[ ! -z "$BOT_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; then
    echo "Stopping bot (PID: $BOT_PID)"
    kill $BOT_PID
    wait $BOT_PID 2>/dev/null
  fi

  if [[ ! -z "$CLIENT_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; then
    echo "Stopping client (PID: $CLIENT_PID)"
    kill $CLIENT_PID
    wait $CLIENT_PID 2>/dev/null
  fi

  if [[ ! -z "$TCPDUMP_PID" ]] && kill -0 $TCPDUMP_PID 2>/dev/null; then
    echo "Stopping tcpdump (PID: $TCPDUMP_PID)"
    kill $TCPDUMP_PID
    wait $TCPDUMP_PID 2>/dev/null
    echo "Packets saved to: ${CAP_FILE_PATH}"
  fi
}
trap clean_up EXIT INT TERM

sleep $DURATION
