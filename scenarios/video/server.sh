#!/usr/bin/env bash

# Video Server Script
# Save as video_server.sh and make executable: chmod +x video_server.sh

# Check if ffmpeg is installed
if ! command -v ffmpeg &>/dev/null; then
  echo "ffmpeg not found. Installing..."
  sudo apt update
  sudo apt install -y ffmpeg
fi

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

# Start HTTP video server (option 1: simple HTTP server)
echo "Starting HTTP video server on port 8080..."
sudo python3 -m http.server 8080 &
HTTP_PID=$!

# Start RTMP server (option 2: for real streaming)
echo "Starting RTMP server on port 1935..."
sudo ffmpeg -re -stream_loop -1 -i "$VIDEO_FILE" -c copy -f flv rtmp://localhost:1935/live/stream &
RTMP_PID=$!

# Start RTMP server application (nginx with rtmp module)
echo "You might want to install nginx with RTMP module for production use:"
echo "sudo apt install -y nginx libnginx-mod-rtmp"

# Wait for user to stop
echo "Video servers running. Press Ctrl+C to stop."
echo "HTTP server: http://$SERVER_IP:8080/$VIDEO_FILE"
echo "RTMP server: rtmp://$SERVER_IP:1935/live/stream"

trap 'echo "Stopping servers..."; kill $HTTP_PID $RTMP_PID; exit' INT
wait
