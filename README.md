# django-app-deploy
Automated deployment for Django Application.

## Requirements

- Ansible Control Node: Debian 12 or later
- Ansible Managed Node: Debian 12 or later with ssh access

## Usage

### Install necessary packages on Ansible Control Node

Run the following commands with root privileges on the Ansible control node:
```bash
apt update
apt install python3 ansible ansible-lint curl
```

### Install `uv` tool for Python package management with a normal user

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

It will install `uv` in `$HOME/.local/bin/uv`. You may need to reload your shell or add this directory to your `PATH` variable.

### Clone the repository

```bash
git clone git@github.com:hdaojin/django-app-deploy.git
cd django-app-deploy
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
# -K is uppercase K, it will prompt for the become password
```

For Ansible managed node:

```bash
uv run play_tasks.py init managed -k -K
uv run play_tasks.py run -r system_init
```


