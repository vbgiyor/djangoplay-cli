"""
Celery worker command.
"""

import subprocess

from dplay.core.repo_detector import ensure_repo
from dplay.environment.venv_detector import ensure_venv


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def worker_command():
    """
    Start Celery worker and beat services.
    """

    ensure_repo()
    ensure_venv()

    subprocess.run(
        ["celery", "-A", "paystream", "worker", "-l", "info"],
        check=True,
    )
