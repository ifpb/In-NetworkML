# Between Packets and Predictions: Analyzing the Overhead of In-Network Machine Learning in Programmable Switches

This repository refers to the article **"Between Packets and Predictions: Analyzing the Overhead of In-Network Machine Learning in Programmable Switches"** as the source code of its methodology.

It shows with details how the virtual network topology is configured, **how a decision tree traffic classifier is trained and implemented into a software-based switch** and how all the required data is collected to fulfill the article's purpose of expoloring the gap left by most articles of this gender, which is to **quantify how impactful this machine learning implementation is for the programmable switch**.

## Repository structure

The repository is structured as follows:

- ansible - Playbook files for configuring each VM.
- scenarios - Scenario specific configuration. Each scenario includes an Ansible playbook for configuration, a startup script, and an optional server script.
- metric_collectoin - Scripts responsible for collecting all metrics used in analysis and model training 
- p4 - Pipeline for the P4 implementation of the trained decision tree.
- plot_scripts - A dedicated directory for all scripts used to plot the article's graphs

## Running the Experiment

### Pre-requisites

- Vagrant
- Oracle VirtualBox
- Pyenv

### Installation

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
