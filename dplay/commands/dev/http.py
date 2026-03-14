"""
HTTP development server command.
"""

import subprocess

from dplay.core.repo_detector import ensure_repo
from dplay.environment.venv_detector import ensure_venv
from dplay.utils.dev_startup import print_environment, restart_celery


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def http_command():
    """
    Start DjangoPlay HTTP development server.

    Starts:
    - Celery worker
    - Celery beat
    - Django development server
    """

    repo_path = ensure_repo()
    python_exec = ensure_venv()

    print_environment(repo_path, python_exec)

    restart_celery()

    print("✔ Django server starting\n")

    print("Server URL:")
    print("http://localhost:3333\n")

    print("Press CTRL+C to stop the server.\n")

    subprocess.run(
        ["python", "manage.py", "runserver", "localhost:3333"],
        check=True,
    )
