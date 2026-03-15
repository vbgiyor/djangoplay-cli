"""
Development command group for djangoplay-cli.

This package contains CLI commands responsible for managing
the local DjangoPlay development environment.

Available commands include:

- dev http     → start Django development server (HTTP)
- dev ssl      → start Django development server (HTTPS)
- dev worker   → start Celery worker
- dev up       → start full development environment
- dev down     → stop development environment
- dev logs     → display development logs

The commands in this package coordinate services such as:

- Django development server
- Celery worker and beat
- Redis
- PostgreSQL

These commands are registered under the `dplay dev` command
group defined in `dplay.cli`.
"""
