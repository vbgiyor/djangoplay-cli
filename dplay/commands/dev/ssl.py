"""
HTTPS development server command.
"""

import subprocess
import sys

from dplay.core.config_loader import load_config
from dplay.core.process_manager import restart_celery, stop_django, wait_for_celery
from dplay.core.repo_detector import ensure_repo
from dplay.environment.venv_detector import ensure_venv
from dplay.utils.browser import open_browser
from dplay.utils.dev_startup import print_environment
from dplay.utils.env_manager import encrypt_env
from dplay.utils.redis_manager import flush_redis
from dplay.utils.ssl_manager import TLSError, ensure_ssl_certificates
from dplay.utils.static_manager import collect_static


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def ssl_command():
    """
    Start DjangoPlay HTTPS development server.
    """

    repo_path = ensure_repo()
    python_exec = ensure_venv()
    config = load_config()

    host = config["site"]["host"]
    port = str(config["site"]["ssl_port"])
    protocol = config["site"]["ssl_protocol"]

    # Set runtime site vars before encrypt_env runs
    import os

    os.environ["SITE_PROTOCOL"] = protocol
    os.environ["SITE_HOST"] = host
    os.environ["SITE_PORT"] = port
    os.environ["SITE_URL"] = config["site"]["ssl_url"]

    login_url = f"{config['site']['ssl_url']}/accounts/login/"

    print_environment(repo_path, python_exec)

    encrypt_env(repo_path, python_exec)
    flush_redis()
    collect_static(repo_path, python_exec)

    try:
        cert_file, key_file = ensure_ssl_certificates()
    except TLSError:
        print("TLS certificate unavailable. Use `dplay http`")
        sys.exit(1)

    restart_celery(repo_path, python_exec)
    wait_for_celery()

    stop_django()

    open_browser(login_url)

    print("Starting Django HTTPS server...")

    try:
        subprocess.run(
            [
                python_exec,
                "manage.py",
                "runserver_plus",
                f"{host}:{port}",
                "--cert-file",
                str(cert_file),
                "--key-file",
                str(key_file),
            ],
            cwd=f"{repo_path}/backend",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode in (-9, -15, -2):
            print("\nDjangoPlay server was stopped. A new session has taken over.")
        else:
            raise
