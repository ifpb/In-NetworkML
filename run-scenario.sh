saida() {
  echo "Usage: ./run-scenario.sh [ scenario | duration ]"
  echo "Available scenarios:"
  ls scenarios
  exit 1
}

set -euo pipefail

if [ -z $1 ] || [ ! -d scenarios/$1 ]; then
  saida
fi

if [[ -z $2 ]]; then
  DURATION=60
elif [[ $2 =~ ^[0-9]+$ ]]; then
  DURATION=$2
else
  echo "Duration must be a positive number"
  exit 1
fi

echo "Rodando cenário $1 com duração de $DURATION"

vagrant up --provision
vagrant ssh-config >ssh_config

ansible-playbook scenarios/$1/server.yml
ansible-playbook scenarios/$1/client.yml

mkdir -p logs
if [[ -e ./scenarios/$1/server.sh ]]; then
  echo "Rodando script do servidor"
  scp -F ./ssh_config ./scenarios/$1/server.sh h2:/tmp
  ssh -F ./ssh_config h2 'sudo nohup bash /tmp/server.sh >/vagrant/logs/server.log 2>/vagrant/logs/server.err & echo $! > /tmp/server.pid' &
fi

if [[ -e ./scenarios/$1/client.sh ]]; then
  echo "Rodando script do client"
  scp -F ./ssh_config ./scenarios/$1/client.sh h1:/tmp
  ssh -F ./ssh_config h1 "sudo DURATION=$DURATION bash /tmp/client.sh > /vagrant/logs/client.log 2>/vagrant/logs/client.err"
fi

if [[ -e ./scenarios/$1/server.sh ]]; then
  echo "Desligando servidor"
  ssh -F ./ssh_config h2 'kill $(cat /tmp/server.pid)'
fi
