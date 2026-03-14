"""
Repository detection utilities.
"""

import subprocess
import sys


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def ensure_repo():
    """
    Ensure command runs inside DjangoPlay repository.

    Returns
    -------
    str
        Repository root path.
    """

    try:
        result = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
        )

        repo_path = result.decode().strip()

        if "djangoplay" not in repo_path.lower():
            raise RuntimeError

        return repo_path

    except Exception:
        print(
            "Error: DjangoPlay repository not detected.\n"
            "Run this command inside the DjangoPlay project directory."
        )
        sys.exit(1)
