set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENARIOS_DIR="${SCRIPT_DIR}/scenarios"
LOGS_DIR="${SCRIPT_DIR}/logs"

saida() {
  echo "Uso: ./run-scenario.sh [ cenário | duração ]"
  echo "Cenários disponíveis:"
  ls scenarios
  exit 1
}

if [ -z $1 ] || [ ! -d scenarios/$1 ]; then
  saida
fi

SCENARIO="$1"
SCENARIO_DIR="${SCENARIOS_DIR}/${SCENARIO}"

if [[ -z $2 ]]; then
  DURATION=60
elif [[ $2 =~ ^[0-9]+$ ]]; then
  DURATION=$2
else
  echo "Duração deve ser um inteiro positivo"
  exit 1
fi

echo "Rodando cenário ${SCENARIO} com duração de ${DURATION}s"

mkdir -p ${LOGS_DIR}

vagrant up --provision
vagrant ssh-config >"${SCRIPT_DIR}/ssh_config"

if [[ -f "${SCENARIO_DIR}/server.yml" ]]; then
  echo "Rodando playbook do servidor"
  ansible-playbook "${SCENARIO_DIR}/server.yml"
fi

if [[ -f "${SCENARIO_DIR}/client.yml" ]]; then
  echo "Rodando playbook do cliente"
  ansible-playbook "${SCENARIO_DIR}/client.yml"
fi

if [[ -f "${SCENARIO_DIR}/server.sh" ]]; then
  echo "Rodando script do servidor"
  scp -F "${SCRIPT_DIR}/ssh_config" "${SCENARIO_DIR}/server.sh" h2:/tmp
  ssh -F "${SCRIPT_DIR}/ssh_config" h2 'sudo nohup bash /tmp/server.sh >/vagrant/logs/server.log 2>/vagrant/logs/server.err & echo $! > /tmp/server.pid' &
fi

if [[ -f "${SCENARIO_DIR}/client.sh" ]]; then
  echo "Rodando script do client com duração de ${DURATION}s"
  scp -F "${SCRIPT_DIR}/ssh_config" "${SCENARIO_DIR}/client.sh" h1:/tmp
  ssh -F "${SCRIPT_DIR}/ssh_config" h1 "sudo DURATION=$DURATION bash /tmp/client.sh | tee /vagrant/logs/client.log 2>/vagrant/logs/client.err"
fi

if [[ -f "${SCENARIO_DIR}/server.sh" ]]; then
  echo "Desligando servidor"
  ssh -F "${SCRIPT_DIR}/ssh_config" h2 'kill $(cat /tmp/server.pid)'
fi
