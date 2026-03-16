"""
Process management utilities.

Responsibility: Celery worker, beat, and Django server lifecycle management.
"""

import os
import subprocess
import sys
import time

from dplay.core.config_loader import load_config


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _celery_env() -> dict:
    """
    Build the environment dict required for Celery subprocesses.

    Reads DJANGO_SETTINGS_MODULE from ~/.dplay/config.yaml so the
    CLI remains decoupled from any hardcoded host application values.
    """

    config = load_config()
    settings_module = config["django"]["settings_module"]

    env = os.environ.copy()
    env["DJANGO_SETTINGS_MODULE"] = settings_module
    return env


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def start_celery(repo_path: str, python_exec: str):
    """
    Start Celery worker and beat as background processes.
    """

    backend_dir = f"{repo_path}/backend"
    env = _celery_env()

    subprocess.Popen(
        [python_exec, "-m", "celery", "-A", "paystream", "worker", "-l", "info"],
        cwd=backend_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.Popen(
        [python_exec, "-m", "celery", "-A", "paystream", "beat", "-l", "info"],
        cwd=backend_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def stop_celery():
    """
    Stop all running Celery worker and beat processes.
    """

    subprocess.run(
        'pkill -9 -f "celery.*paystream" 2>/dev/null || true',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        'pkill -9 -f "celery.*beat" 2>/dev/null || true',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def restart_celery(repo_path: str, python_exec: str):
    """
    Stop existing Celery processes and start fresh ones.
    """

    print("Starting Celery worker + beat...")

    stop_celery()
    start_celery(repo_path, python_exec)


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def stop_django():
    """
    Stop any running Django development server process.

    Matches both runserver and runserver_plus processes to ensure
    a clean port before starting a new server instance.
    """

    print("Stopping existing Django server...")

    subprocess.run(
        'pkill -9 -f "manage.py runserver" 2>/dev/null || true',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        'pkill -9 -f "manage.py runserver_plus" 2>/dev/null || true',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("✔ Previous server stopped\n")


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def wait_for_celery(timeout: int = 20):
    """
    Poll until a Celery worker process is detectable or timeout expires.

    Celery is a runtime dependency of the host application — tasks
    such as password reset and report handling depend on it being
    active before the Django server starts accepting requests.
    """

    deadline = time.time() + timeout

    sys.stdout.write("Waiting for Celery...")
    sys.stdout.flush()

    while time.time() < deadline:
        result = subprocess.run(
            ["pgrep", "-f", "celery.*paystream"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode == 0:
            print("Celery ready ✅")
            return

        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)

    print("\nWarning: Celery did not start within timeout — continuing anyway.")
