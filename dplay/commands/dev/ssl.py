"""
HTTPS development server command.
"""

import subprocess

from dplay.core.repo_detector import ensure_repo
from dplay.environment.venv_detector import ensure_venv
from dplay.utils.dev_startup import print_environment, restart_celery


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def ssl_command():
    """
    Start DjangoPlay HTTPS development server.

    Uses runserver_plus when available.
    """

    repo_path = ensure_repo()
    python_exec = ensure_venv()

    print_environment(repo_path, python_exec)

    restart_celery()

    print("✔ Django HTTPS server starting\n")

    print("Server URL:")
    print("https://localhost:9999\n")

    try:
        subprocess.run(
            ["python", "manage.py", "runserver_plus", "localhost:9999"],
            check=True,
        )
    except Exception:
        subprocess.run(
            ["python", "manage.py", "runserver", "localhost:9999"],
            check=True,
        )
