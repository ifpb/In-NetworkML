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
- Python 3.9

### Instalation

1. Clone the repository

```bash
git clone https://github.com/ifpb/In-NetworkML.git
cd In-NetworkML
```

2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install pip dependencies

```bash
pip install -r requirements.txt
```
