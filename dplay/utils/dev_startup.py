"""
Development startup helpers.

Responsibility: CLI environment summary display only.

All other startup concerns are handled by dedicated utilities:
  - env_manager.py     → environment encryption
  - redis_manager.py   → Redis flush
  - static_manager.py  → static file collection
  - process_manager.py → Celery lifecycle
  - ssl_manager.py     → TLS certificate management
  - browser.py         → browser open
"""


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def print_environment(repo_path: str, python_exec: str):
    """
    Print CLI environment summary.
    """

    print("\nDjangoPlay CLI\n")
    print(f"Repository:   {repo_path}")
    print(f"Python:       {python_exec}")
    print("Environment:  development\n")
