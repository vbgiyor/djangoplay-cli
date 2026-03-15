"""
CLI entrypoint for djangoplay-cli.

This module defines the root CLI application and registers
all command groups.

Implemented commands in v0.2:

- dplay dev http
- dplay dev ssl
- dplay dev worker
- dplay system doctor
- dplay system reset
- dplay shell
"""

import typer

from dplay.commands.dev.http import http_command
from dplay.commands.dev.ssl import ssl_command
from dplay.commands.dev.worker import worker_command
from dplay.commands.system.doctor import doctor_command
from dplay.commands.system.reset import reset_command

app = typer.Typer(help="DjangoPlay CLI")

dev_app = typer.Typer(help="Development commands")
env_app = typer.Typer(help="Environment diagnostics")

dev_app.command("http")(http_command)
dev_app.command("ssl")(ssl_command)
dev_app.command("worker")(worker_command)
env_app.command("doctor")(doctor_command)
env_app.command("reset")(reset_command)

app.add_typer(dev_app, name="dev")
app.add_typer(env_app, name="system")


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def main():
    """
    CLI entrypoint used by the console script.
    """
    app()


if __name__ == "__main__":
    main()
