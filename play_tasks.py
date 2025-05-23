#!/usr/bin/env python3
from pathlib import Path
from typing import List
import sys
from enum import Enum

import ansible_runner
import typer
from typing_extensions import Annotated
from rich import print


app = typer.Typer(help="Ansible Runner CLI for executing playbooks and roles")

def run_ansible_tasks(
        private_data_dir: Path,
        playbook: str | None = None,
        role: str | None = None,
        tags: list[str] | None = None,
        extravars: dict[str, str] | None = None,
):
    """
    Run ansible playbook or role with given parameters using ansible_runner.run()

    Args:
        private_data_dir: Ansible Runner private data directory
        playbook: playbook file to execute
        role: role name to execute
        tags: tags list to execute
        extravars: extra variables for ansible, heigh priority

    Returns:
        Ansible Runner execution result
    """

    run_kwargs = {
        "private_data_dir": private_data_dir,
        "tags": tags,
        "extravars": extravars,
    }

    if playbook:
        run_kwargs["playbook"] = playbook
    elif role:
        run_kwargs["role"] = role
    else:
        raise ValueError("Either playbook or role must be provided.")

    r = ansible_runner.run(**run_kwargs)

    print(f"[bold]Status:[/bold] {r.status}, [bold]Return code:[/bold] {r.rc}")

    return r


def run_command_playbook(
        executable_cmd: str | None = "ansible-playbook",
        cmdline_args: list[str] = 'site.yml',
):
    """
    Run ansible-playbook command with given parameters.

    Args:
        executable_cmd: ansible-playbook command to execute
        cmdline_args: command line arguments for ansible-playbook
        input_fd: input file descriptor
        output_fd: output file descriptor
        error_fd: error file descriptor

    Returns:
        None
    """
    out, err, rc = ansible_runner.run_command(
        executable_cmd=executable_cmd,
        cmdline_args=cmdline_args,
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,      
    )
    print(f"[bold]Return code:[/bold] {rc}")
    print(f"[bold]Out:[/bold] {out}")
    print(f"[bold]Error:[/bold] {err}")
    
    return out, err, rc


@app.command("run")
def cli_run(
        private_data_dir: Annotated[Path, typer.Argument(exists=True, dir_okay=True, file_okay=False, help="Ansible Runner private data directory")] = Path.cwd(),
        playbook: Annotated[str, typer.Option("-p", "--playbook", help="invoke an ansible playbook")] = '',
        role: Annotated[str, typer.Option("-r", "--role", help="invoke an ansible role")] = '',
        tags: Annotated[str, typer.Option("-t", "--tags", help="tags to run, multiple tags separated by comma")] = '',
        # extravars: Annotated[dict[str, str], typer.Option(help="Extra variables for ansible")] = {},
):
    """
    Run ansible playbook or role with given parameters using ansible_runner.run()
    """

    # playbook and role must be specified and only one of them can be specified
    if not playbook and not role:
        print("[bold red]ERROR[/bold red]: Either playbook or role must be provided.")
        raise typer.Exit(code=1)
    if playbook and role:
        print("[bold red]ERROR[/bold red]: Only one of playbook or role can be specified.")
        raise typer.Exit(code=2)
    
    run_ansible_tasks(private_data_dir, playbook, role, tags)


class AnsibleNodeType(str, Enum):
    """
    Ansible node type
    """
    CONTROL_NODE = "control"
    MANAGED_NODE = "managed"


@app.command("init")
def initialize_ansible_control_node(
    node: Annotated[AnsibleNodeType, typer.Argument(help="Ansible node type")],
    ask_pass: Annotated[bool, typer.Option("-k", "--ask-pass", is_eager=True, help="ask for connection password")] = False,
    ask_become_pass: Annotated[bool, typer.Option("-K", "--ask-become-pass", is_eager=True, help="ask for privilege escalation password")] = False,
):
    """
    Initialize ansible control node with given parameters.
    """

    if node == AnsibleNodeType.CONTROL_NODE:
        playbook = "project/ansible_control.yml"
        inventory = "localhost,"
    elif node == AnsibleNodeType.MANAGED_NODE:
        playbook = "project/ansible_managed.yml"
        inventory = "inventory/hosts"

    cmdline_args = [playbook, "-i", inventory]
    
    if ask_pass:
        cmdline_args.append("-k")
    if ask_become_pass:
        cmdline_args.append("-K")

    executable_cmd = "ansible-playbook"

    run_command_playbook(
        executable_cmd=executable_cmd,
        cmdline_args=cmdline_args,
    )


if __name__ == "__main__":
    app()