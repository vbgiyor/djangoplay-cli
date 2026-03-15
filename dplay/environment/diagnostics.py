"""
Environment diagnostics utilities.
"""

import shutil
import socket
import sys


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def check_python():
    """Verify Python version."""

    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        return True, "Python version OK"
    return False, "Python >=3.11 required"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def check_redis():
    """Check Redis availability."""

    try:
        sock = socket.create_connection(("127.0.0.1", 6379), timeout=1)
        sock.close()
        return True, "Redis reachable"
    except Exception:
        return False, "Redis not reachable"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def check_postgres():
    """Check Postgres availability."""

    try:
        sock = socket.create_connection(("127.0.0.1", 5432), timeout=1)
        sock.close()
        return True, "Postgres reachable"
    except Exception:
        return False, "Postgres not reachable"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def check_celery():
    """Check Celery availability."""

    if shutil.which("celery"):
        return True, "Celery available"
    return False, "Celery not installed"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def run_diagnostics():
    """Run all environment checks."""

    checks = [
        check_python,
        check_redis,
        check_postgres,
        check_celery,
    ]

    results = []

    for check in checks:
        results.append(check())

    return results
