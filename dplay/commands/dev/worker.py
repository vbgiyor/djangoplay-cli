"""
Celery worker command.
"""

import os
import subprocess

from dplay.core.config_loader import load_config
from dplay.core.repo_detector import ensure_repo
from dplay.environment.venv_detector import ensure_venv


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def worker_command():
    """
    Start Celery worker in the foreground.
    """

    repo_path = ensure_repo()
    python_exec = ensure_venv()
    config = load_config()

    env = os.environ.copy()
    env["DJANGO_SETTINGS_MODULE"] = config["django"]["settings_module"]

    subprocess.run(
        [python_exec, "-m", "celery", "-A", "paystream", "worker", "-l", "info"],
        cwd=f"{repo_path}/backend",
        env=env,
        check=True,
    )
