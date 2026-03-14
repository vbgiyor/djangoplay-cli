"""
CLI entrypoint for djangoplay-cli.

This module defines the root CLI application and registers
all command groups.

Implemented commands in v0.1:

- dplay dev http
- dplay dev ssl
- dplay dev worker
"""

import typer

from dplay.commands.dev.http import http_command
from dplay.commands.dev.ssl import ssl_command
from dplay.commands.dev.worker import worker_command

app = typer.Typer(help="DjangoPlay CLI")

dev_app = typer.Typer(help="Development commands")

dev_app.command("http")(http_command)
dev_app.command("ssl")(ssl_command)
dev_app.command("worker")(worker_command)

app.add_typer(dev_app, name="dev")


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def main():
    """
    CLI entrypoint used by the console script.

    This wrapper ensures compatibility with Python packaging
    and avoids exposing the Typer object directly.
    """
    app()


if __name__ == "__main__":
    main()
