"""
CLI entrypoint for djangoplay-cli.

This module defines the root CLI application and registers
all command groups.
"""

from importlib.metadata import version

import typer

from dplay.commands.dev.http import http_command
from dplay.commands.dev.logs import logs_command
from dplay.commands.dev.ssl import ssl_command
from dplay.commands.dev.worker import worker_command
from dplay.commands.system.doctor import doctor_command
from dplay.commands.system.reset import reset_command

app = typer.Typer(help="DjangoPlay CLI", add_completion=False)


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------


def get_cli_version() -> str:
    """
    Retrieve CLI version from installed package metadata.
    """

    try:
        return version("djangoplay-cli")
    except Exception:
        return "unknown"


# ------------------------------------------------------------------
# DEV COMMAND GROUP
# ------------------------------------------------------------------

dev_app = typer.Typer(help="Development commands", invoke_without_command=True)


@dev_app.callback(invoke_without_command=True)
def dev_callback(ctx: typer.Context):
    """
    Development commands. Defaults to HTTP server when no subcommand given.
    """

    if ctx.invoked_subcommand is None:
        http_command()


dev_app.command("http")(http_command)
dev_app.command("ssl")(ssl_command)
dev_app.command("worker")(worker_command)

app.add_typer(dev_app, name="dev")

# ------------------------------------------------------------------
# SYSTEM COMMAND GROUP
# ------------------------------------------------------------------

system_app = typer.Typer(help="System environment commands")

system_app.command("doctor")(doctor_command)
system_app.command("reset")(reset_command)

app.add_typer(system_app, name="system")

# ------------------------------------------------------------------
# LOG COMMAND
# ------------------------------------------------------------------

app.command("logs")(logs_command)

# -------------------------------------------------------------
# GLOBAL OPTIONS
# ------------------------------------------------------------------


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version_flag: bool = typer.Option(None, "--version", "-v", is_eager=True),
):
    """
    CLI entrypoint used by the console script.

    This wrapper ensures compatibility with Python packaging
    and avoids exposing the Typer object directly and handles
    global CLI option such as --version.
    """

    if version_flag:
        typer.echo(get_cli_version())
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def main():
    app()
