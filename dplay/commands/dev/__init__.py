"""
Development command group for djangoplay-cli.

This package contains CLI commands responsible for managing
the local DjangoPlay development environment.

Available commands include:

- dplay http     → start Django development server (HTTP)
- dplay ssl      → start Django development server (HTTPS)
- dplay worker   → start Celery worker
- dplay certs    → regenerate SSL certificates
- dplay logs     → stream application logs

The commands in this package coordinate services such as:

- Django development server
- Celery worker and beat
- Redis
- PostgreSQL

These commands are registered at the root `dplay` command
group defined in `dplay.cli`.
"""
