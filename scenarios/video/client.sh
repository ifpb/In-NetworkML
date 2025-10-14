#!/usr/bin/env bash

# Test scenario duration in seconds, default = 60s
if [ -z "${DURATION}" ]; then
  DURATION=60
else
  DURATION=${DURATION}
fi

SERVER_IP="192.168.56.102"
VIDEO_URL_RTMP="rtmp://$SERVER_IP:1935/live/stream"
INTERFACE="eth1"

CAP_FILE="video_$(date +%s).pcap"
PCAP_DIR="/vagrant/pcap"
CAP_FILE_PATH="${PCAP_DIR}/${CAP_FILE}"

# Function to get client IP
get_client_ip() {
  hostname -I | awk '{print $1}'
}

# Function to start packet capture
start_capture() {
  echo "Starting packet capture on interface $INTERFACE..."
  echo "Capturing to file: $CAP_FILE_PATH"
  mkdir -p /vagrant/pcap
  sudo tcpdump -i $INTERFACE -w "$CAP_FILE_PATH" host "$SERVER_IP" &
  TCPDUMP_PID=$!
  sleep 2
}

# Function to stop packet capture
stop_capture() {
  echo "Stopping packet capture..."
  sudo kill $TCPDUMP_PID
  sleep 2
  echo "Packet capture saved to $CAP_FILE_PATH"

  # Show capture statistics
  if [ -f "$CAP_FILE_PATH" ]; then
    echo "Capture file info:"
    tcpdump -r "$CAP_FILE_PATH" -q | head -10
  fi
}

run_client() {
  echo "Starting client"
  while true; do
    ffmpeg -i "$VIDEO_URL_RTMP" -t 10 -f null - 2>/dev/null &
    echo $! > /tmp/ffmpeg.pid
    wait $(cat /tmp/ffmpeg.pid)
    sleep 0.5
  done
}

clean_up() {
  FFMPEG_PID=$(cat /tmp/ffmpeg.pid)
  if [[ ! -z "$FFMPEG_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; then
    echo "Stopping client (PID: $FFMPEG_PID)"
    kill $FFMPEG_PID
    wait $FFMPEG_PID 2>/dev/null
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

start_capture

run_client &
CLIENT_PID=$!

sleep $DURATION
