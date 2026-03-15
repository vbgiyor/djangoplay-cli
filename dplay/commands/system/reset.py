"""
Environment reset command.
"""

import subprocess


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def reset_command():
    """
    Reset development environment.
    """

    print("\nResetting development environment\n")

    subprocess.run(
        'pkill -9 -f "celery.*paystream" 2>/dev/null || true',
        shell=True,
    )

    subprocess.run(
        'pkill -9 -f "celery.*beat" 2>/dev/null || true',
        shell=True,
    )

    print("✔ Celery processes stopped")

    subprocess.run(
        "redis-cli flushall",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("✔ Redis flushed\n")
