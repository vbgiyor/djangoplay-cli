"""
Start full development environment.
"""

import subprocess

from dplay.core.process_manager import start_celery


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def up_command():
    """
    Start Redis, Celery and Django services.
    """

    print("Starting DjangoPlay development environment\n")

    start_celery()

    subprocess.Popen(["python", "manage.py", "runserver", "localhost:3333"])

    print("Environment is up")
