#!/usr/bin/env bash

set -euo pipefail

# Test scenario duration in seconds, default = 60s
DURATION="${DURATION:-60}"
CAP_FILE="${CAP_FILE:-web_$(date +%s).pcap}"
PCAP_DIR="${PCAP_DIR:-/vagrant/pcap}"

CAP_FILE_PATH="${PCAP_DIR}/${CAP_FILE}"
CSV_FILE="${PCAP_DIR}/flow_completion_time.csv"

INTERFACE="eth1"
REMOTE_USER="vagrant"
REMOTE_HOST="192.168.56.102"
SSH_OPTS="-o StrictHostKeyChecking=no"

TEST_DIR="/tmp/test_files"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

start_packet_capture() {

  log_info "Starting packet capture..."

  mkdir -p $PCAP_DIR >/dev/null 2>&1
  # Start packet capture in background
  if tcpdump -i $INTERFACE -w ${CAP_FILE_PATH} >/dev/null 2>&1 & then
    local capture_pid=$!
    log_success "Packet capture started with PID: $capture_pid"
    echo "$capture_pid" >"/tmp/scp_test_capture.pid"

    # Wait a moment for capture to initialize
    sleep 2
    return 0
  else
    log_error "Failed to start packet capture script"
    return 1
  fi
}

# Stop packet capture
stop_packet_capture() {
  local pid_file="/tmp/scp_test_capture.pid"

  if [[ -f "$pid_file" ]]; then
    local capture_pid=$(cat "$pid_file")
    if kill -0 "$capture_pid" 2>/dev/null; then
      log_info "Stopping packet capture (PID: $capture_pid)"
      kill "$capture_pid" 2>/dev/null
      wait "$capture_pid" 2>/dev/null || true
      rm -f "$pid_file"
      log_success "Packet capture stopped"
    fi
  fi
}

# Transfer files via SCP
transfer_files() {
  log_info "Starting SCP file from to ${REMOTE_USER}@${REMOTE_HOST}:${TEST_DIR}"

  mkdir "${TEST_DIR}" 2>/dev/null || true

  # Transfer each file individually to capture separate SCP sessions
  for category in text binary archive; do
    local category_dir="$TEST_DIR/$category"

    for file in $(ssh ${SSH_OPTS} ${REMOTE_USER}@${REMOTE_HOST} "ls ${category_dir}" 2>/dev/null); do
      local filename=$(basename "$file")
      log_info "Transferring: $filename"

      start_time=$(date +%s.%N)
      scp "${REMOTE_USER}@${REMOTE_HOST}:${category_dir}/$filename" ${TEST_DIR} &
      echo $! >/tmp/scp.pid

      wait $(cat /tmp/scp.pid)

      end_time=$(date +%s.%N)

      timestamp=$(date +%s%3N)
      fct=$(echo "$end_time - $start_time" | bc)

      echo "${timestamp},${filename},${fct}" >>${CSV_FILE}

      # delay
      sleep 0.5
    done
  done
}

run_client() {
  while true; do
    transfer_files
  done
}

# Start packet capture
if ! start_packet_capture; then
  exit 1
fi

# CSV headers
echo "timestamp,filename,flow_completion_time" >${CSV_FILE}

# Transfer files
run_client &
CLIENT_PID=$!

cleanup() {
  SCP_PID=$(cat /tmp/scp.pid)
  if [[ ! -z "$SCP_PID" ]] && kill -0 $SCP_PID 2>/dev/null; then
    echo "Stopping scp (PID: $SCP_PID)"
    kill $SCP_PID
    wait $SCP_PID 2>/dev/null
  fi

  if [[ ! -z "$CLIENT_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; then
    echo "Stopping client (PID: $CLIENT_PID)"
    kill $CLIENT_PID
    wait $CLIENT_PID 2>/dev/null
  fi

  stop_packet_capture
}

trap cleanup EXIT INT TERM KILL

sleep $DURATION
