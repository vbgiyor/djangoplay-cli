"""
Static files utility.

Responsibility: collect static files via manage.py subprocess.
The CLI treats manage.py as a black box — no Django internals imported.
"""

import subprocess
import sys


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def collect_static(repo_path: str, python_exec: str):
    """
    Clear and collect static files via manage.py collectstatic.

    Parameters
    ----------
    repo_path : str
        Absolute path to the repository root.
    python_exec : str
        Python executable from the active virtual environment.
    """

    print("Clearing static files...")

    result = subprocess.run(
        [python_exec, "manage.py", "collectstatic", "--noinput", "--clear"],
        cwd=f"{repo_path}/backend",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode != 0:
        print("Error: collectstatic failed.")
        sys.exit(1)

    print("Collecting static files...")
