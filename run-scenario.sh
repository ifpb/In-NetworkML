saida() {
	echo "Usage: ./run-scenario.sh [ scenario | duration ]"
	echo "Available scenarios:"
	ls scenarios
	exit 1	
}

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
vagrant ssh-config > ssh_config

ansible-playbook scenarios/$1/server.yml
ansible-playbook -e "DURATION=$DURATION" scenarios/$1/client.yml
