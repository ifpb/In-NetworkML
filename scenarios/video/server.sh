#!/usr/bin/env bash

# Check if video file exists
VIDEO_FILE="sample.mp4"
if [ ! -f "$VIDEO_FILE" ]; then
  echo "Video file not found. Creating a sample video..."
  # Create a simple test video (30 seconds)
  ffmpeg -f lavfi -i testsrc=duration=30:size=640x480:rate=30 "$VIDEO_FILE"
fi

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "Starting video server on $SERVER_IP"

# Start RTMP server
echo "Starting RTMP server on port 1935..."
run_server() {
  while [[ true ]]; do
    ffmpeg -re -stream_loop -1 -i "$VIDEO_FILE" -listen 1 -c copy -f flv rtmp://localhost/live/stream
  done
}

run_server &
RTMP_PID=$!

# Wait for user to stop
echo "RTMP server: rtmp://$SERVER_IP:1935/live/stream"

trap 'echo "Stopping server..."; kill $RTMP_PID; exit' INT
wait
