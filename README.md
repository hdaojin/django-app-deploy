# django-app-deploy
Automated deployment for Django Application.



## Usage

### Install necessary packages on Ansible Control Node

```bash
# run command using root user
apt update
apt install python3 ansible ansible-lint 
```

### Install `uv` tool for Python package management

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install required Python packages

```bash
uv sync
```

### Initialize the Ansible control node and Ansible managed node

Try `uv run play_tasks.py --help` for help.

```bash
uv run play_tasks.py --help
uv run play_tasks.py init --help
uv run play_tasks.py run --help
```

For Ansible control node:

```bash
uv run play_tasks.py init control -K
```

For Ansible managed node:

```bash
uv run play_tasks.py init managed -k -K
```