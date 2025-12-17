#!/usr/bin/env bash

set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENARIOS_DIR="${SCRIPT_DIR}/scenarios"
LOGS_DIR="${SCRIPT_DIR}/logs"

START_TIME=$(date +%s)

# Generate timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

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

total_to_kms() {
  local total="$1"

  local hours=$((total / 3600))
  local minutes=$(((total % 3600) / 60))
  local seconds=$((total % 60))

  printf "%02d:%02d:%02d" "$hours" "$minutes" "$seconds"
}

elapsed_time() {
  local now=$(date +%s)
  local elapsed_time="$((now - START_TIME))"

  echo $(total_to_kms $elapsed_time)
}

if [[ "$1" == "-ml" ]]; then
	USE_ML=1
	shift 1
else
	USE_ML=0
fi

saida() {
  echo "Uso: ./run-scenario.sh [ cenário | duração ]"
  echo "Cenários disponíveis:"
  ls scenarios
  exit 1
}

if [ -z $1 ] || [ ! -d scenarios/$1 ]; then
  saida
fi


time_convert() {
    input="$1"
    total=0
    temp="$input"
    
    while [[ $temp =~ ([0-9]+)([hms]) ]]; do
        val="${BASH_REMATCH[1]}"
        unit="${BASH_REMATCH[2]}"
        
        case "$unit" in
            h) total=$((total + val * 3600)) ;;
            m) total=$((total + val * 60)) ;;
            s) total=$((total + val)) ;;
        esac

        temp="${temp#*${BASH_REMATCH[0]}}"
    done
    echo "$total"
}

SCENARIO="$1"
SCENARIO_DIR="${SCENARIOS_DIR}/${SCENARIO}"

if [[ -z "$2" ]]; then
	log_info "Usando valor de tempo padrão: 60 segundos"
	DURATION=60
elif [[ $2 =~ ^([0-9]+h)?([0-9]+m)?([0-9]+s)?$ ]] && [[ -n "$2" ]]; then
	DURATION=$(time_convert $2)
else
	log_error "Formato de tempo inválido (XhYmZx)"
	exit 1
fi

log_info "Rodando cenário ${SCENARIO} com duração de ${DURATION}s"

mkdir -p ${LOGS_DIR}

USE_ML="$USE_ML" vagrant up --provision
vagrant ssh-config >"${SCRIPT_DIR}/ssh_config"

if [[ -f "${SCENARIO_DIR}/server.yml" ]]; then
  log_info "Rodando playbook do servidor"
  ansible-playbook "${SCENARIO_DIR}/server.yml"
fi

if [[ -f "${SCENARIO_DIR}/client.yml" ]]; then
  log_info "Rodando playbook do cliente"
  ansible-playbook "${SCENARIO_DIR}/client.yml"
fi

if [[ "$USE_ML" == 1 ]]; then
	OUTPUT_DIR="/vagrant/metrics/${SCENARIO}_ML_${TIMESTAMP}"
else
	OUTPUT_DIR="/vagrant/metrics/${SCENARIO}_${TIMESTAMP}"
fi

export OUTPUT_DIR
PCAP_DIR="${OUTPUT_DIR}"
CAP_FILE="packets.pcap"


# Create output dir
ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo mkdir -p "${OUTPUT_DIR}" 2>/dev/null"

# Start Telemetry and iperf
${SCRIPT_DIR}/get-telemetry.sh >/dev/null &
INT_PID=$!

${SCRIPT_DIR}/run-iperf.sh &
IPERF_PID=$!

log_info "Rodando script de coleta de métricas de sistema do switch"
scp -F "${SCRIPT_DIR}/ssh_config" "switch_resource_metrics.sh" s1:/tmp >/dev/null
ssh -F "${SCRIPT_DIR}/ssh_config" s1 "OUTPUT_DIR=${OUTPUT_DIR} /tmp/switch_resource_metrics.sh" &
SWITCH_PID=$!

if [[ "$USE_ML" == 1 ]]; then
  ssh -F "${SCRIPT_DIR}/ssh_config" s1 "/vagrant/code/ml_metrics.py" &
  ML_METRICS_PID=$!
fi

cleanup() {
  rm -f "${SCRIPT_DIR}/server_ready" 2>/dev/null

  kill $INT_PID 2>/dev/null
  kill $IPERF_PID 2>/dev/null
  ssh -F "${SCRIPT_DIR}/ssh_config" s1 "sudo pkill -2 -f /tmp/switch_resource_metrics.sh"
  kill $SWITCH_PID 2>/dev/null
  if [[ "$USE_ML" == 1 ]]; then
    kill $ML_METRICS_PID 2>/dev/null
    wait $ML_METRICS_PID 2>/dev/null
  fi
  
  wait $INT_PID 2>/dev/null
  wait $IPERF_PID 2>/dev/null
  wait $SWITCH_PID 2>/dev/null
}

trap cleanup EXIT TERM INT

if [[ -f "${SCENARIO_DIR}/server.sh" ]]; then
  log_info "Rodando script do servidor"
  scp -F "${SCRIPT_DIR}/ssh_config" "${SCENARIO_DIR}/server.sh" h2:/tmp >/dev/null
  ssh -F "${SCRIPT_DIR}/ssh_config" h2 'sudo bash /tmp/server.sh 2>/vagrant/logs/server.err | tee /vagrant/logs/server.log' &
  SERVER_PID=$!

  log_info "Esperando o servidor estar pronto"
  while [[ ! -f "${SCRIPT_DIR}/server_ready" ]]; do
    log_warning "Not ready $(elapsed_time)" >&2
    sleep 1
  done
fi

START_TIME=$(date +%s)

if [[ -f "${SCENARIO_DIR}/client.sh" ]]; then
  log_info "Rodando script do client com duração de ${DURATION}s"
  scp -F "${SCRIPT_DIR}/ssh_config" "${SCENARIO_DIR}/client.sh" h1:/tmp >/dev/null
  ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo PCAP_DIR=${OUTPUT_DIR} CAP_FILE='packets.pcap' DURATION=$DURATION bash /tmp/client.sh 2>/vagrant/logs/client.err | tee /vagrant/logs/client.log" &
  CLIENT_PID=$!
  while [[ ! -f "$CLIENT_PID" ]] && kill -0 $CLIENT_PID 2>/dev/null; do
    log_info "Tempo decorrido: $(elapsed_time)/$(total_to_kms $DURATION)"
    sleep 1
  done
fi

if [[ -f "${SCENARIO_DIR}/server.sh" ]]; then
  if [[ ! -z "$SERVER_PID" ]] && kill -0 $SERVER_PID 2>/dev/null; then
    log_info "Desligando servidor (PID: $SERVER_PID)"
    kill $SERVER_PID
    wait $SERVER_PID 2>/dev/null
  fi
fi

#ssh -F "${SCRIPT_DIR}/ssh_config" s1 "SCENARIO=$SCENARIO /vagrant/code/editcmatrix 2> /dev/null"
