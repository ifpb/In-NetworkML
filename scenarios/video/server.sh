#!/usr/bin/env bash

# Check if video file exists
VIDEO_FILE="sample.mp4"
if [ ! -f "$VIDEO_FILE" ]; then
  echo "Video file not found. Creating a sample video..."
  # Create a simple test video (30 seconds)
  ffmpeg -f lavfi -i testsrc=duration=30:size=640x480:rate=30 "$VIDEO_FILE"
fi

# Start RTMP server
echo "Starting RTMP server on port 1935..."
#-hide_banner -loglevel error
ffmpeg -re -stream_loop -1 -i "$VIDEO_FILE" -c copy -f flv rtmp://localhost/live/stream &
RTMP_PID=$!

# Server is Ready
touch /vagrant/server_ready

trap 'echo "Stopping server..."; kill $RTMP_PID 2>/dev/null || true; exit 0' INT TERM KILL EXIT
wait $RTMP_PID
