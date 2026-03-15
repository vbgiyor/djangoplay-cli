"""
Environment diagnostics command.
"""

from dplay.core.repo_detector import ensure_repo
from dplay.environment.diagnostics import run_diagnostics
from dplay.environment.venv_detector import ensure_venv


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def doctor_command():
    """
    Run environment diagnostics.
    """

    ensure_repo()
    ensure_venv()

    print("\nEnvironment Diagnostics\n")

    results = run_diagnostics()

    for ok, message in results:
        if ok:
            print(f"✔ {message}")
        else:
            print(f"✖ {message}")

    print("")
