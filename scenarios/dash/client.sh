#!/usr/bin/env bash

# Test scenario duration in seconds, default = 60s
DURATION="${DURATION:-60}"
CAP_FILE="${CAP_FILE:-web_$(date +%s).pcap}"
PCAP_DIR="${PCAP_DIR:-/vagrant/pcap}"
METRICS_FILE="$PCAP_DIR""/http_metrics.csv"

CAP_FILE_PATH="${PCAP_DIR}/${CAP_FILE}"

SERVER_IP="192.168.56.102"
INTERFACE="eth1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to start packet capture
start_capture() {
  echo "Starting packet capture on interface $INTERFACE..."
  echo "Capturing to file: $CAP_FILE_PATH"
  mkdir -p /vagrant/pcap
  sudo tcpdump -i $INTERFACE -w "$CAP_FILE_PATH" host "$SERVER_IP" and not tcp port 5201 and not ip proto 253 &
  TCPDUMP_PID=$!
}

# Function to stop packet capture
stop_capture() {
  if [[ ! -z "$TCPDUMP_PID" ]] && kill -0 $TCPDUMP_PID 2>/dev/null; then
    echo "Stopping tcpdump (PID: $TCPDUMP_PID)"
    sudo kill $TCPDUMP_PID
    wait $TCPDUMP_PID 2>/dev/null
    echo "Packets saved to: ${CAP_FILE_PATH}"
  fi
}

clean_up() {
  stop_capture

  if [[ ! -z "$CLIENT_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; then
    echo "Stopping client (PID: $CLIENT_PID)"
    sudo kill $CLIENT_PID
    wait $CLIENT_PID 2>/dev/null
  fi

  sudo mv logs*.txt "${PCAP_DIR}/logs.txt"
}
trap clean_up EXIT INT TERM

start_capture

node player-mpegdash/index.js &
CLIENT_PID=$!

wait $CLIENT_PID

stop_capture
