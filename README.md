# djangoplay-cli

Maintained by [DjangoPlay](https://djangoplay.org)

![PyPI](https://img.shields.io/pypi/v/djangoplay-cli)
![Python](https://img.shields.io/pypi/pyversions/djangoplay-cli)
![License](https://img.shields.io/badge/license-MIT-green)
![Django](https://img.shields.io/badge/django-4.2-green)
![Lint](https://img.shields.io/badge/lint-ruff-informational)

**djangoplay-cli** is a developer command-line interface for managing local
development environments within the **DjangoPlay ecosystem**.

The CLI simplifies common developer workflows such as:

- starting HTTP and HTTPS development servers
- regenerating SSL certificates
- managing Celery workers
- validating environment dependencies
- resetting development services
- streaming application logs
- orchestrating local development processes

The goal is to provide a **simple, predictable, and portable developer tool**
without introducing complex infrastructure dependencies.

---

# Philosophy

This project follows several guiding principles:

* **Minimal configuration**
* **No secrets in the repository**
* **Clear command structure**
* **Stable developer experience**
* **Incremental releases**
* **Developer-first ergonomics**

The CLI is designed to remove repetitive setup tasks so developers can focus
on application development instead of environment management.

---

# Supported Platforms

| Platform | Status |
|----------|--------|
| macOS | Supported |
| Linux | Supported |
| Ubuntu | Supported |
| Windows (WSL) | Supported |
| Windows native | Limited |

---

# Installation

Install from PyPI:

```bash
pip install djangoplay-cli
```

Verify installation:

```bash
dplay --version
```

Example output:

```
1.0.5
```

---

# CLI Overview

```
dplay
├── http
├── ssl
├── certs
├── logs
│
├── dev
│    └── worker
│
└── system
     ├── doctor
     └── reset
```

---

# Development Commands

These commands manage the Django development environment.

---

## Start HTTP development server

```bash
dplay http
```

Performs the following automatically:

* encrypts environment variables from `~/.dplay/`
* flushes Redis cache
* collects static files
* restarts Celery worker and beat
* waits until Celery is ready
* stops any existing Django server on the configured port
* opens the browser
* starts the Django development server

The server URL is automatically derived from `~/.dplay/config.yaml`.

Example:

```yaml
http_protocol: http
http_port: 3333
http_url: localhost
```

---

## Start HTTPS development server

```bash
dplay ssl
```

Performs the same startup sequence as `dplay http`, plus:

* checks for SSL certificates under `~/.dplay/ssl/`
* generates certificates if necessary
* automatically trusts certificates on macOS, Linux, and WSL
* launches Django using `runserver_plus`

The HTTPS URL is read from your configuration.

If certificates cannot be generated:

```
TLS certificate unavailable. Use dplay http
```

---

## Start Celery worker

```bash
dplay dev worker
```

Starts the Celery worker in the foreground.

---

## Regenerate SSL certificates

```bash
dplay certs
```

Regenerates SSL certificates from the current configuration without restarting
the development server.

Useful after adding new subdomains:

```yaml
subdomains:
  extra_domains:
    - issues.localhost
    - docs.localhost
```

Then run:

```bash
dplay certs
dplay ssl
```

The generated certificate is automatically trusted on supported platforms.

---

## Stream application logs

```bash
dplay logs
dplay logs [APP]
```

Streams and pretty-prints application logs with colorized output by log level.

Examples:

```bash
dplay logs
dplay logs users
dplay logs mailer --level ERROR
dplay logs django --no-follow -n 100
```

Options:

| Option | Default | Description |
|--------|---------|-------------|
| `APP` | `django` | Application log to stream |
| `--lines`, `-n` | `50` | Historical lines shown initially |
| `--level`, `-l` | — | Filter by log level |
| `--follow` / `--no-follow` | follow | Stream new log entries |

Applications are discovered automatically from `backend/logs/`.

---

# System Commands

## Environment diagnostics

```bash
dplay system doctor
```

Checks:

* Python version
* Redis availability
* PostgreSQL availability
* Celery installation

---

## Reset development environment

```bash
dplay system reset
```

Performs:

* stops Celery workers
* stops Celery beat
* flushes Redis

---

# CLI Help

```bash
dplay --help
```

Development commands:

```bash
dplay dev --help
```

System commands:

```bash
dplay system --help
```

---

# Project Structure

```
djangoplay-cli/

dplay/
├── commands/
├── core/
├── environment/
└── utils/
```

## Architecture

| Layer | Responsibility |
|-------|----------------|
| CLI Commands | User-facing commands |
| Core | Repository detection, process management |
| Environment | Environment validation |
| Utils | SSL, logging, Redis, browser, startup orchestration |

The modular architecture keeps the CLI maintainable while allowing new commands
to be added with minimal coupling.

---

# Development Setup

Clone the repository:

```bash
git clone https://github.com/binaryfleet/djangoplay-cli.git
cd djangoplay-cli
```

Install locally:

```bash
pip install -e .
```

Install development tools:

```bash
pip install ruff pytest
```

Run linting:

```bash
ruff check .
```

Run tests:

```bash
pytest
```

---

# Security

This project follows strict security practices:

* no credentials stored in the repository
* no secrets generated automatically
* no credentials written to disk
* SSL certificates generated only for local development

---

# Versioning

This project follows **Semantic Versioning**.

```
v0.x  Experimental
v1.x  Stable
```

---

# License

Licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.