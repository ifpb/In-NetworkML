#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-/vagrant/metrics}"
OUTPUT_FILE="${OUTPUT_DIR}/iperf.json"
H2_IP="192.168.56.102"

ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo mkdir -p "${OUTPUT_DIR}" 2>/dev/null"

ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo iperf3 -s -J > ${OUTPUT_FILE}" &
RECEIVER_PID=$!

sleep .2

ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo iperf3 -t 0 -c ${H2_IP} >/dev/null 2>&1" &
SENDER_PID=$!

cleanup() {
  ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo pkill -2 -f iperf3"
  ssh -F "${SCRIPT_DIR}/ssh_config" h2 "sudo pkill -2 -f iperf3"

  kill $SENDER_PID 2>/dev/null || true
  kill $RECEIVER_PID 2>/dev/null || true

  wait $SENDER_PID 2>/dev/null
  wait $RECEIVER_PID 2>/dev/null
}

trap cleanup INT TERM EXIT KILL

wait $SENDER_PID
