#!/usr/bin/env bash

# Video Client with Packet Capture
# Save as video_client.sh and make executable: chmod +x video_client.sh

# Configuration
SERVER_IP="127.0.0.1" # Replace with your server VM IP
VIDEO_URL_HTTP="http://$SERVER_IP:8080/sample.mp4"
VIDEO_URL_RTMP="rtmp://$SERVER_IP:1935/live/stream"
CAPTURE_FILE="video_stream.pcap"
INTERFACE="lo" # Change to your network interface

# # Check if tcpdump is installed
# if ! command -v tcpdump &>/dev/null; then
#   echo "tcpdump not found. Installing..."
#   sudo apt update
#   sudo apt install -y tcpdump
# fi
#
# # Check if ffmpeg is installed
# if ! command -v ffmpeg &>/dev/null; then
#   echo "ffmpeg not found. Installing..."
#   sudo apt update
#   sudo apt install -y ffmpeg
# fi

# Function to get client IP
get_client_ip() {
  hostname -I | awk '{print $1}'
}

# Function to start packet capture
start_capture() {
  echo "Starting packet capture on interface $INTERFACE..."
  echo "Capturing to file: $CAPTURE_FILE"
  # sudo tcpdump -i $INTERFACE -w "$CAPTURE_FILE" host "$SERVER_IP" &
  # TCPDUMP_PID=$!
  sleep 2
}

# Function to stop packet capture
stop_capture() {
  echo "Stopping packet capture..."
  # sudo kill $TCPDUMP_PID
  sleep 2
  echo "Packet capture saved to $CAPTURE_FILE"

  # # Show capture statistics
  # if [ -f "$CAPTURE_FILE" ]; then
  #   echo "Capture file info:"
  #   tcpdump -r "$CAPTURE_FILE" -q | head -10
  # fi
}

# Function to test HTTP streaming
test_http_stream() {
  echo "Testing HTTP video stream..."
  start_capture

  # Stream video using ffmpeg (without displaying)
  timeout 30 ffmpeg -i "$VIDEO_URL_HTTP" -f null - &
  FFMPEG_PID=$!

  wait $FFMPEG_PID
  stop_capture
}

# Function to test RTMP streaming
test_rtmp_stream() {
  echo "Testing RTMP video stream..."
  start_capture

  # Stream video using ffmpeg
  timeout 30 ffmpeg -i "$VIDEO_URL_RTMP" -f null - &
  FFMPEG_PID=$!

  wait $FFMPEG_PID
  stop_capture
}

# Function for continuous testing
continuous_test() {
  echo "Starting continuous video streaming test..."
  echo "Server IP: $SERVER_IP"
  echo "Client IP: $(get_client_ip)"
  echo "Press Ctrl+C to stop"

  start_capture

  # Continuous while loop to request video
  COUNTER=0
  while true; do
    COUNTER=$((COUNTER + 1))
    echo "Streaming attempt #$COUNTER - $(date)"

    # Try HTTP first, then RTMP if HTTP fails
    timeout 30 ffmpeg -i "$VIDEO_URL_HTTP" -t 10 -f null - 2>/dev/null
    if [ $? -ne 0 ]; then
      echo "HTTP failed, trying RTMP..."
      timeout 30 ffmpeg -i "$VIDEO_URL_RTMP" -t 10 -f null - 2>/dev/null
    fi

    sleep 5
  done
}

# Main menu
echo "Video Streaming Client with Packet Capture"
echo "=========================================="
echo "1) Test HTTP streaming (30 seconds)"
echo "2) Test RTMP streaming (30 seconds)"
echo "3) Continuous streaming test"
echo "4) Quit"

read -p "Select option [1-4]: " choice

case $choice in
1)
  test_http_stream
  ;;
2)
  test_rtmp_stream
  ;;
3)
  continuous_test
  ;;
4)
  echo "Exiting..."
  exit 0
  ;;
*)
  echo "Invalid option"
  exit 1
  ;;
esac

# Cleanup on exit
trap 'stop_capture; exit' INT
