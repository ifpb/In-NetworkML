# Between Packets and Predictions: Analyzing the Overhead of In-Network Machine Learning in Programmable Switches

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Repository structure

The repository is structured as follows:

- ansible - playbook files for configuring each VM.
- scenarios - scenario specific configuration. Each scenario includes an Ansible playbook for configuration, a startup script, and an optional server script.

## Running the Experiment

### Pre-requisites

- Vagrant
- Oracle VirtualBox
- Pyenv

### Instalation

1. Clone the repository

```bash
git clone https://github.com/ifpb/In-NetworkML.git
cd In-NetworkML
```

2. Create a python3.9 virtual environment

```bash
pyenv install 3.9.19
pyenv global 3.9.19

python3 -m venv .venv
source .venv/bin/activate
```
- Alternatively, if you're in a debian based distribution, you get python3.9 through its official tar ball

```bash
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

wget https://www.python.org/ftp/python/3.9.19/Python-3.9.19.tgz
tar -xf Python-3.9.19.tgz
cd Python-3.9.19
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

python3.9 -m venv .venv
source .venv/bin/activate
```

3. Install pip dependencies

```bash
pip install -r requirements.txt
```
