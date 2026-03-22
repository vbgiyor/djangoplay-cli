"""
Log streaming command.
"""

import typer

from dplay.core.repo_detector import ensure_repo
from dplay.utils.log_manager import (
    DEFAULT_APP,
    DEFAULT_LINES,
    get_log_dir,
    resolve_log_file,
    stream_logs,
)


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def logs_command(
    app: str | None = typer.Argument(
        None,
        help="App name to tail e.g. users, django, mailer. Defaults to django.",
    ),
    lines: int = typer.Option(
        DEFAULT_LINES,
        "--lines",
        "-n",
        help="Number of historical lines to show on startup.",
    ),
    level: str | None = typer.Option(
        None,
        "--level",
        "-l",
        help="Filter by log level e.g. ERROR, WARNING, INFO, DEBUG.",
    ),
    follow: bool = typer.Option(
        True,
        "--follow/--no-follow",
        "-f/-F",
        help="Stream new log lines in real time. Enabled by default.",
    ),
):
    """
    Stream development logs with pretty-printed, colorized output.

    Defaults to django.log. Pass an app name to tail a specific log.

    Examples:

        dplay dev logs
        dplay dev logs users
        dplay dev logs mailer --level ERROR
        dplay dev logs django --no-follow --lines 100
    """

    target_app = app or DEFAULT_APP

    repo_path = ensure_repo()
    log_dir = get_log_dir(repo_path)

    try:
        log_file = resolve_log_file(log_dir, target_app)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e

    typer.echo(f"\nDjangoPlay Logs — {target_app}\n")

    stream_logs(
        log_file=log_file,
        lines=lines,
        level_filter=level,
        follow=follow,
    )
