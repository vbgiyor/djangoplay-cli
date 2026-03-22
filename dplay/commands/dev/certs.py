"""
SSL certificate management command.
"""

from dplay.utils.ssl_manager import TLSError, regenerate_ssl_certificates


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def certs_command():
    """
    Regenerate local SSL certificates from current config.

    Reads subdomains.extra_domains from ~/.dplay/config.yaml and rebuilds
    the self-signed certificate with the correct Subject Alternative
    Names. Use this after adding new subdomains to config.yaml.

    Automatically trusts the new certificate in the macOS Keychain.
    """

    try:
        cert_file, key_file = regenerate_ssl_certificates()
    except TLSError as e:
        print(f"Error: {e}")
        raise SystemExit(1) from e

    print(f"\nCertificate: ~/.dplay/ssl/{cert_file.name}")
    print(f"Key:         ~/.dplay/ssl/{key_file.name}")

    print("\nRun `dplay dev ssl` to start the HTTPS server with the new certificate.")
