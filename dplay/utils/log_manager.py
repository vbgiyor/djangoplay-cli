"""
Log management utilities.

Responsibility: log file resolution, parsing, filtering, and
pretty-printed streaming for the `dplay dev logs` command.

Log format produced by CustomFormatter:
    IST DEBUG 2026-03-22 08:56:12,123 <LogRecord: name, lineno, "message">
"""

import re
import sys
import time
from pathlib import Path

# ------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------

DEFAULT_APP = "django"
DEFAULT_LINES = 50

# Maps log levels to ANSI color codes
LEVEL_COLORS = {
    "DEBUG": "\033[2m",  # dim
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # bold red
}
RESET = "\033[0m"

# Matches: IST DEBUG 2026-03-22 08:56:12,123 <LogRecord: name, lineno, "message">
_LOG_PATTERN = re.compile(
    r"^IST\s+(?P<level>\w+)\s+"
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s+"
    r"<LogRecord:\s*(?P<logger>[^,]+),\s*(?P<lineno>\d+),\s*\"(?P<message>.*)\"\s*>"
    r"(?:\s*\[(?P<exc>.+)\])?$"
)


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def get_log_dir(repo_path: str) -> Path:
    """
    Resolve the log directory from the repository root.

    Parameters
    ----------
    repo_path : str
        Absolute path to the repository root as returned by ensure_repo().

    Returns
    -------
    Path
        Absolute path to {repo_path}/backend/logs/.
    """

    return Path(repo_path) / "backend" / "logs"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def get_available_apps(log_dir: Path) -> list[str]:
    """
    Return a sorted list of app names derived from log files on disk.

    Scans for *.log files at runtime so new applications are discovered
    automatically without requiring CLI changes.

    Parameters
    ----------
    log_dir : Path
        Path to the log directory.

    Returns
    -------
    list[str]
        Sorted list of app names e.g. ['apidocs', 'django', 'users'].
    """

    return sorted(f.stem for f in log_dir.glob("*.log") if f.is_file())


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def resolve_log_file(log_dir: Path, app: str) -> Path:
    """
    Resolve and validate the log file path for a given app name.

    Parameters
    ----------
    log_dir : Path
        Path to the log directory.
    app : str
        Application name to look up e.g. 'users', 'django'.

    Returns
    -------
    Path
        Absolute path to the log file.

    Raises
    ------
    FileNotFoundError
        If no log file exists for the given app name.
    """

    log_file = log_dir / f"{app}.log"

    if not log_file.exists():
        available = get_available_apps(log_dir)
        cols = "    ".join(available)
        raise FileNotFoundError(f"No log file found for '{app}'\n\nAvailable apps:\n  {cols}")

    return log_file


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _parse_line(line: str) -> dict | None:
    """
    Parse a single log line into its components.

    Parameters
    ----------
    line : str
        Raw log line from the log file.

    Returns
    -------
    dict | None
        Parsed components or None if the line does not match the
        expected log format.
    """

    match = _LOG_PATTERN.match(line.strip())

    if not match:
        return None

    return {
        "level": match.group("level"),
        "timestamp": match.group("timestamp"),
        "logger": match.group("logger").strip(),
        "lineno": match.group("lineno"),
        "message": match.group("message"),
        "exc": match.group("exc"),
    }


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _colorize(parsed: dict) -> str:
    """
    Format a parsed log entry as a colorized string for terminal output.

    Parameters
    ----------
    parsed : dict
        Parsed log components as returned by _parse_line().

    Returns
    -------
    str
        ANSI-colorized log line ready for printing.
    """

    level = parsed["level"]
    color = LEVEL_COLORS.get(level, "")

    level_str = f"{color}{level:<8}{RESET}"
    ts_str = f"\033[2m{parsed['timestamp']}\033[0m"
    logger = f"\033[36m{parsed['logger']}\033[0m"  # cyan
    message = parsed["message"]

    line = f"{level_str} {ts_str}  {logger}  {message}"

    if parsed.get("exc"):
        line += f"\n         \033[31m{parsed['exc']}\033[0m"

    return line


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _tail_lines(log_file: Path, n: int) -> list[str]:
    """
    Return the last n lines from a log file efficiently.

    Uses a seek-from-end strategy to avoid reading the entire file
    into memory — suitable for large rotating log files.

    Parameters
    ----------
    log_file : Path
        Path to the log file.
    n : int
        Number of lines to return from the end of the file.

    Returns
    -------
    list[str]
        Last n lines of the file as strings.
    """

    with open(log_file, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        block = 8192
        data = b""
        pos = size

        while len(data.splitlines()) <= n and pos > 0:
            pos = max(pos - block, 0)
            f.seek(pos)
            data = f.read(size - pos)

        return data.decode("utf-8", errors="replace").splitlines()[-n:]


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def stream_logs(
    log_file: Path,
    lines: int,
    level_filter: str | None,
    follow: bool,
):
    """
    Stream and pretty-print log output to stdout.

    Prints the last `lines` entries first, then continuously polls
    the file for new content when follow=True. Applies optional
    level filtering before rendering.

    Parameters
    ----------
    log_file : Path
        Path to the log file to stream.
    lines : int
        Number of historical lines to display on startup.
    level_filter : str | None
        If provided, only lines matching this level are shown
        e.g. 'ERROR'. Case-insensitive.
    follow : bool
        If True, continue polling the file for new lines after
        the initial output. If False, print and exit.
    """

    level_upper = level_filter.upper() if level_filter else None

    def _emit(line: str):
        """Parse, filter, and print a single log line."""
        parsed = _parse_line(line)

        if parsed is None:
            # Unparseable line — print raw dimmed
            if not level_upper:
                print(f"\033[2m{line}\033[0m")
            return

        if level_upper and parsed["level"] != level_upper:
            return

        print(_colorize(parsed))

    # Print historical lines
    for line in _tail_lines(log_file, lines):
        _emit(line)

    if not follow:
        return

    # Stream new lines
    print(f"\n\033[2mWatching {log_file.name} — press Ctrl+C to stop\033[0m\n")

    with open(log_file, encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)  # seek to end

        try:
            while True:
                where = f.tell()
                line = f.readline()

                if line and line.endswith("\n"):
                    _emit(line)
                else:
                    # No complete line yet — seek back and wait
                    f.seek(where)
                    time.sleep(0.2)

        except KeyboardInterrupt:
            print("\n\033[2mStopped.\033[0m")
            sys.exit(0)
