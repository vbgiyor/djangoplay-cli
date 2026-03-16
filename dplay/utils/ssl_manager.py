"""
SSL certificate management for local development.

Responsibility: ensure self-signed TLS certificates exist under
~/.dplay/ssl/ and generate them via openssl if absent.

Certificate paths are returned to ssl_command() and passed
directly to runserver_plus via --cert-file / --key-file.
Without these flags runserver_plus silently serves HTTP.
"""

import platform
import subprocess
from pathlib import Path

SSL_DIR = Path.home() / ".dplay" / "ssl"
CERT_FILE = SSL_DIR / "localhost.crt"
KEY_FILE = SSL_DIR / "localhost.key"


class TLSError(RuntimeError):
    """Raised when TLS certificates are unavailable and cannot be created."""


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def ensure_ssl_certificates() -> tuple[Path, Path]:
    """
    Ensure SSL certificate and key exist for localhost.

    Returns
    -------
    tuple[Path, Path]
        (cert_file, key_file) ready for runserver_plus.

    Raises
    ------
    TLSError
        If certificates are missing and cannot be generated.
    """

    if CERT_FILE.exists() and KEY_FILE.exists():
        print("Using existing SSL certificates")
        return CERT_FILE, KEY_FILE

    print("SSL certificates not found — generating...")

    SSL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-keyout",
                str(KEY_FILE),
                "-out",
                str(CERT_FILE),
                "-days",
                "825",
                "-nodes",
                "-subj",
                "/CN=localhost",
                "-addext",
                "subjectAltName=DNS:localhost,IP:127.0.0.1",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            raise TLSError("openssl exited with a non-zero status.")

    except FileNotFoundError as err:
        raise TLSError("openssl not found on this system.") from err

    if not CERT_FILE.exists() or not KEY_FILE.exists():
        raise TLSError("Certificate files were not created.")

    print(f"✔ SSL certificates created → {SSL_DIR}")

    _trust_certificate_macos()

    return CERT_FILE, KEY_FILE


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _trust_certificate_macos():
    """
    Add the generated certificate to the macOS System Keychain as trusted.

    Runs only on macOS. Prompts for sudo password once.
    After this, Chrome and Safari trust the cert permanently
    and will not show ERR_CERT_AUTHORITY_INVALID for localhost.
    No-op on Linux and Windows.
    """

    if platform.system() != "Darwin":
        return

    print("Trusting certificate in macOS Keychain (requires sudo)...")

    result = subprocess.run(
        [
            "sudo",
            "security",
            "add-trusted-cert",
            "-d",
            "-r",
            "trustRoot",
            "-k",
            "/Library/Keychains/System.keychain",
            str(CERT_FILE),
        ]
    )

    if result.returncode == 0:
        print("✔ Certificate trusted in macOS Keychain")
    else:
        print("Warning: Could not trust certificate automatically.")
        print(
            f"Run manually to resolve browser warnings:\n"
            f"  sudo security add-trusted-cert -d -r trustRoot"
            f" -k /Library/Keychains/System.keychain {CERT_FILE}"
        )
