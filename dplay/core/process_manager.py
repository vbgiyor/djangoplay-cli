"""
Process management utilities.
"""

import subprocess


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def start_celery():
    """
    Start celery worker and beat.
    """

    subprocess.Popen(["celery", "-A", "paystream", "worker", "-l", "info"])

    subprocess.Popen(["celery", "-A", "paystream", "beat", "-l", "info"])


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def stop_celery():
    """
    Stop running celery workers.
    """

    subprocess.run(
        'pkill -9 -f "celery.*paystream" 2>/dev/null || true',
        shell=True,
    )

    subprocess.run(
        'pkill -9 -f "celery.*beat" 2>/dev/null || true',
        shell=True,
    )
