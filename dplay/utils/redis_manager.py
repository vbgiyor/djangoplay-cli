"""
Redis utility.

Responsibility: flush Redis cache via redis-cli subprocess.
"""

import subprocess
import sys


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def flush_redis():
    """
    Flush all Redis keys using redis-cli.
    """

    print("Flushing Redis...")

    result = subprocess.run(
        ["redis-cli", "flushall"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error: Failed to flush Redis. Is Redis running?")
        sys.exit(1)

    print(result.stdout.strip() or "OK")
