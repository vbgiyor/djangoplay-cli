"""
Virtual environment detection utilities.
"""

import os
import sys


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def ensure_venv():
    """
    Ensure Python virtual environment is active.

    Returns
    -------
    str
        Python executable path.
    """

    if "VIRTUAL_ENV" not in os.environ:
        print("Error: Virtual environment not active.")
        sys.exit(1)

    return sys.executable
