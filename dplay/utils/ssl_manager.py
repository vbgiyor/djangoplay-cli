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

from dplay.core.config_loader import load_config

SSL_DIR = Path.home() / ".dplay" / "ssl"
CERT_FILE = SSL_DIR / "localhost.crt"
KEY_FILE = SSL_DIR / "localhost.key"


class TLSError(RuntimeError):
    """Raised when TLS certificates are unavailable and cannot be created."""


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _build_san() -> str:
    """
    Build Subject Alternative Name list dynamically.

    Always includes *.localhost wildcard to cover all localhost subdomains
    (e.g. issues.localhost, api.localhost) without requiring config changes.
    """

    config = load_config()
    host = config["site"]["host"]

    san_entries = {
        "DNS:localhost",
        "DNS:*.localhost",  # ← add this line
        "IP:127.0.0.1",
    }

    if host:
        san_entries.add(f"DNS:{host}")
        parts = host.split(".")
        if len(parts) > 1:
            parent = ".".join(parts[1:])
            san_entries.add(f"DNS:*.{parent}")

    # Explicit subdomains for Chrome (does not honour *.localhost wildcards)
    extra_domains = config.get("subdomains", {}).get("extra_domains", [])
    for domain in extra_domains:
        san_entries.add(f"DNS:{domain}")

    return ",".join(sorted(san_entries))


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

    san = _build_san()

    def cert_has_san(cert_file: Path, expected_san: str) -> bool:
        """
        Verify that an existing certificate contains all expected SAN entries.

        Compares each entry individually rather than the full SAN string to
        avoid false mismatches caused by openssl's comma-space formatting vs
        the comma-only format produced by _build_san().

        Parameters
        ----------
        cert_file : Path
            Path to the certificate file to inspect.
        expected_san : str
            Comma-separated SAN string as returned by _build_san(),
            e.g. 'DNS:*.localhost,DNS:issues.localhost,IP:127.0.0.1'

        Returns
        -------
        bool
            True only if every expected SAN entry is present in the certificate.
        """

        try:
            out = subprocess.check_output(
                ["openssl", "x509", "-in", str(cert_file), "-noout", "-text"],
                stderr=subprocess.DEVNULL,
            ).decode()
        except Exception:
            return False

        expected_entries = [e.strip() for e in expected_san.split(",")]

        return all(entry.replace("IP:", "IP Address:") in out for entry in expected_entries)

    # regenerate if missing or SAN mismatch
    if CERT_FILE.exists() and KEY_FILE.exists() and cert_has_san(CERT_FILE, san):
        print("Using existing SSL certificates")
        return CERT_FILE, KEY_FILE

    print("SSL certificates not found or SAN mismatch — generating...")

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
                f"subjectAltName={san}",
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
    _trust_certificate_linux()
    _trust_certificate_wsl()

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


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _trust_certificate_linux():
    """
    Add the generated certificate to the Linux system trust store.

    Copies the certificate into /usr/local/share/ca-certificates/ and
    runs update-ca-certificates to register it system-wide. Requires
    sudo. Supports Debian, Ubuntu, and derivatives.

    Warns and continues if the trust step fails — the server will still
    start but browsers may show a certificate warning until the cert is
    trusted manually.

    No-op on non-Linux platforms.
    """

    if platform.system() != "Linux":
        return

    print("Trusting certificate in Linux system store (requires sudo)...")

    dest = Path("/usr/local/share/ca-certificates/djangoplay-localhost.crt")

    copy_result = subprocess.run(
        ["sudo", "cp", str(CERT_FILE), str(dest)],
    )

    if copy_result.returncode != 0:
        print("Warning: Could not copy certificate to system store.")
        print(
            f"Run manually to resolve browser warnings:\n"
            f"  sudo cp {CERT_FILE} {dest}\n"
            f"  sudo update-ca-certificates"
        )
        return

    update_result = subprocess.run(
        ["sudo", "update-ca-certificates"],
    )

    if update_result.returncode == 0:
        print("✔ Certificate trusted in Linux system store")
    else:
        print("Warning: Could not run update-ca-certificates automatically.")
        print("Run manually to resolve browser warnings:\n  sudo update-ca-certificates")


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def _trust_certificate_wsl():
    """
    Add the generated certificate to the Windows trust store from WSL.

    Detects WSL by inspecting /proc/version for 'microsoft' or 'WSL'.
    Locates certutil.exe via the Windows System32 path mounted under
    /mnt/c/ and registers the certificate in the Windows certificate
    store so that Chrome and Edge on the Windows host trust it.

    Warns and continues if certutil.exe is not found or the trust step
    fails — the server will still start but browsers may show a
    certificate warning until the cert is trusted manually.

    No-op when not running inside WSL.
    """

    if platform.system() != "Linux":
        return

    try:
        proc_version = Path("/proc/version").read_text().lower()
    except Exception:
        return

    if "microsoft" not in proc_version and "wsl" not in proc_version:
        return

    print("WSL detected — trusting certificate in Windows certificate store...")

    certutil = Path("/mnt/c/Windows/System32/certutil.exe")

    if not certutil.exists():
        print("Warning: certutil.exe not found at expected WSL path.")
        print(
            f"Run manually in a Windows terminal to resolve browser warnings:\n"
            f"  certutil -addstore -f Root {CERT_FILE}"
        )
        return

    result = subprocess.run(
        [str(certutil), "-addstore", "-f", "Root", str(CERT_FILE)],
    )

    if result.returncode == 0:
        print("✔ Certificate trusted in Windows certificate store")
    else:
        print("Warning: Could not trust certificate automatically in Windows store.")
        print(
            f"Run manually in a Windows terminal to resolve browser warnings:\n"
            f"  certutil -addstore -f Root {CERT_FILE}"
        )


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def regenerate_ssl_certificates() -> tuple[Path, Path]:
    """
    Force-regenerate SSL certificates from current ~/.dplay/config.yaml.

    Deletes any existing certificate and key under ~/.dplay/ssl/ and
    creates a fresh self-signed certificate whose Subject Alternative
    Names reflect the current ssl.extra_domains list in config.yaml.

    This is the programmatic equivalent of:
        rm -rf ~/.dplay/ssl/
        dplay dev ssl

    Returns
    -------
    tuple[Path, Path]
        (cert_file, key_file) paths to the newly created certificate.

    Raises
    ------
    TLSError
        If openssl is unavailable or certificate generation fails.
    """

    print("Removing existing SSL certificates...")

    CERT_FILE.unlink(missing_ok=True)
    KEY_FILE.unlink(missing_ok=True)

    print("✔ Existing certificates removed\n")

    return ensure_ssl_certificates()
