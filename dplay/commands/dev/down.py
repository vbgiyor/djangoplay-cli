"""
Stop development environment.
"""

from dplay.core.process_manager import stop_celery


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def down_command():
    """
    Stop all development services.
    """

    print("Stopping DjangoPlay services")

    stop_celery()

    print("Services stopped")
