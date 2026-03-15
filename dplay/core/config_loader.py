"""
Configuration loader for DjangoPlay CLI.

Loads configuration from ~/.dplay/config.yaml
and secrets from ~/.dplay/.secrets
"""

import os
from pathlib import Path

import yaml

CONFIG_DIR = Path.home() / ".dplay"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
SECRETS_FILE = CONFIG_DIR / ".secrets"


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def load_config():
    """
    Load YAML configuration file.
    """

    if not CONFIG_FILE.exists():
        raise RuntimeError("Missing configuration file ~/.dplay/config.yaml")

    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def load_secrets():
    """
    Load secrets into environment variables.
    """

    if not SECRETS_FILE.exists():
        return

    with open(SECRETS_FILE) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)

            os.environ[key] = value
