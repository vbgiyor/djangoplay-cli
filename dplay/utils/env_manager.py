"""
Environment encryption utility.

Responsibility: invoke the host application's encrypt_env.py
as a subprocess. The CLI has no knowledge of its internals.
"""

import subprocess
import sys
from pathlib import Path


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def encrypt_env(repo_path: str, python_exec: str):
    """
    Encrypt .env by running the host application's encrypt_env.py.

    Parameters
    ----------
    repo_path : str
        Absolute path to the repository root.
    python_exec : str
        Python executable from the active virtual environment.
    """

    print("Encrypting environment variables...")

    encrypt_script = Path(repo_path) / "backend" / "paystream" / "security" / "encrypt_env.py"

    result = subprocess.run(
        [python_exec, str(encrypt_script)],
        cwd=f"{repo_path}/backend",
    )

    if result.returncode != 0:
        print("Error: Failed to encrypt environment variables.")
        sys.exit(1)
