"""
CLI entrypoint for djangoplay-cli.

This module defines the root CLI application and registers
all command groups.
"""

from importlib.metadata import version

import typer

from dplay.commands.dev.certs import certs_command
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
# SERVER COMMANDS (promoted from dev group)
# ------------------------------------------------------------------

app.command("http")(http_command)
app.command("ssl")(ssl_command)
app.command("worker")(worker_command)
app.command("certs")(certs_command)

# ------------------------------------------------------------------
# LOG COMMAND
# ------------------------------------------------------------------

app.command("logs")(logs_command)

# ------------------------------------------------------------------
# SYSTEM COMMAND GROUP
# ------------------------------------------------------------------

system_app = typer.Typer(help="System environment commands")

system_app.command("doctor")(doctor_command)
system_app.command("reset")(reset_command)

app.add_typer(system_app, name="system")

# ------------------------------------------------------------------
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
