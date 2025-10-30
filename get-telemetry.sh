#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-/vagrant/metrics}"
H2_IP="192.168.56.102"

ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo mkdir -p "${OUTPUT_DIR}" 2>/dev/null"

ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo /vagrant/code/receive.py -o ${OUTPUT_DIR}/telemetry.csv" &
RECEIVER_PID=$!

ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo /vagrant/code/send.py ${H2_IP} 2>/dev/null" &
SENDER_PID=$!

cleanup() {
  ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo pkill -2 -f send.py"
  ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo pkill -2 -f receive.py"

  kill $SENDER_PID 2>/dev/null || true
  kill $RECEIVER_PID 2>/dev/null || true

  wait $SENDER_PID 2>/dev/null
  wait $RECEIVER_PID 2>/dev/null
}

trap cleanup INT TERM EXIT KILL

wait $RECEIVER_PID
