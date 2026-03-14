"""
Development startup helpers.

Shared utilities used by development commands such as:

- dev http
- dev ssl
"""

import subprocess


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def print_environment(repo_path: str, python_exec: str):
    """
    Print CLI environment summary.
    """

    print("\nDjangoPlay CLI\n")

    print(f"Repository:   {repo_path}")
    print(f"Python:       {python_exec}")
    print("Environment:  development\n")


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def restart_celery():
    """
    Stop existing celery processes and start fresh ones.
    """

    print("Stopping existing Celery workers...")

    # File support 0.1
    subprocess.run(
        'pkill -9 -f "celery.*paystream" 2>/dev/null || true',
        shell=True,
    )

    subprocess.run(
        'pkill -9 -f "celery.*beat" 2>/dev/null || true',
        shell=True,
    )

    print("✔ Existing Celery processes cleared\n")

    print("Starting services...\n")

    subprocess.Popen(
        ["celery", "-A", "paystream", "worker", "-l", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("✔ Celery worker started")

    subprocess.Popen(
        ["celery", "-A", "paystream", "beat", "-l", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("✔ Celery beat started\n")
