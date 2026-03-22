# djangoplay-cli

![PyPI](https://img.shields.io/pypi/v/djangoplay-cli)
![Python](https://img.shields.io/pypi/pyversions/djangoplay-cli)
![License](https://img.shields.io/pypi/l/djangoplay-cli)
![Django](https://img.shields.io/badge/django-4.2-green)
![Lint](https://img.shields.io/badge/lint-ruff-informational)

**djangoplay-cli** is a developer command-line interface for managing local
development environments within the **DjangoPlay ecosystem**.

The CLI simplifies common developer workflows such as:

- starting the development server
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
|--------|--------|
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
1.0.4
```

---

# CLI Overview

The CLI is organized into command groups.
```
dplay
 ├── dev
 │    ├── http
 │    ├── ssl
 │    ├── certs
 │    ├── worker
 │    └── logs
 │
 ├── system
 │    ├── doctor
 │    └── reset
 │
 └── logs
```

---

# Development Commands

These commands manage the Django development environment.

---

### Start HTTP development server
```
dplay dev http
```

Performs the following steps automatically:

* encrypts environment variables from `~/.dplay/`
* flushes Redis cache
* collects static files
* restarts Celery worker and beat
* waits until Celery is ready
* stops any existing Django server on the port
* opens the browser
* starts the Django HTTP development server

Server URL:
```
http://localhost:3333
```

---

### Start HTTPS development server
```
dplay dev ssl
```

Performs the same steps as `dplay dev http`, plus:

* checks for SSL certificates under `~/.dplay/ssl/`
* generates self-signed certificates if absent
* trusts the certificate in the system keychain automatically
  (macOS Keychain, Linux system store, or Windows store via WSL)
* starts the server via `runserver_plus` with the certificate and key

Server URL:
```
https://localhost:9999
```

> If SSL certificates cannot be created, the CLI exits with:
> `TLS certificate unavailable. Use dplay dev http`

---

### Default command

Running `dplay dev` without a subcommand starts the HTTP server:
```
dplay dev
```

---

### Start Celery worker
```
dplay dev worker
```

Starts the Celery worker for the DjangoPlay application in the foreground.

---

### Regenerate SSL certificates
```
dplay dev certs
```

Regenerates local SSL certificates from the current `~/.dplay/config.yaml`.
Use this after adding new subdomains to `subdomains.extra_domains` in config.

Automatically trusts the new certificate in the system keychain on macOS,
Linux, and WSL. No server restart required.

To add subdomain coverage, update `~/.dplay/config.yaml`:
```yaml
subdomains:
  extra_domains:
    - issues.localhost
    - docs.localhost
```

Then run:
```
dplay dev certs
dplay dev ssl
```

---

### Stream application logs
```
dplay dev logs
dplay dev logs [APP]
```

Streams and pretty-prints application logs with colorized output by log level.
Defaults to `django.log`. Pass an app name to tail a specific log file.
Available apps are discovered automatically from `backend/logs/`.
```
dplay dev logs                            # django.log, last 50 lines, follow
dplay dev logs users                      # users.log, last 50 lines, follow
dplay dev logs mailer --level ERROR       # errors only, follow
dplay dev logs django --no-follow -n 100  # last 100 lines, exit
```

Options:

| Option | Default | Description |
|---|---|---|
| `APP` | `django` | App name e.g. users, mailer, frontend |
| `--lines / -n` | `50` | Historical lines shown on startup |
| `--level / -l` | None | Filter by level: DEBUG INFO WARNING ERROR CRITICAL |
| `--follow / --no-follow` | follow | Stream new lines in real time |

Also available as `dplay logs` at the top level.

---

# System Commands

System commands validate and reset the development environment.

### Run environment diagnostics
```
dplay system doctor
```

Checks:

* Python version
* Redis availability
* PostgreSQL availability
* Celery installation

Example output:
```
Environment Diagnostics

✔ Python version OK
✔ Redis reachable
✔ Postgres reachable
✔ Celery available
```

---

### Reset development environment
```
dplay system reset
```

Actions performed:

* stop running Celery workers
* stop Celery beat processes
* flush Redis cache

---

# CLI Help

Show CLI help:
```
dplay --help
```

Show development commands:
```
dplay dev --help
```

Show system commands:
```
dplay system --help
```

---

# Project Structure
```
djangoplay-cli/

dplay/
  commands/
  core/
  environment/
  utils/
```

### Architecture Layers

| Layer        | Responsibility                              |
| ------------ | ------------------------------------------- |
| CLI Commands | user-facing commands                        |
| Core         | repository detection, process manager       |
| Environment  | environment validation                      |
| Utils        | reusable helpers (ssl, logs, redis, static) |

This modular architecture keeps the CLI maintainable as new features are added.

---

# Development Setup

Clone repository:
```
git clone https://github.com/binaryfleet/djangoplay-cli.git
cd djangoplay-cli
```

Install in editable mode:
```
pip install -e .
```

Install development tools:
```
pip install ruff pytest
```

Run lint checks:
```
ruff check .
```

Run tests:
```
pytest
```

---

# Security Principles

This project follows strict security practices:

* no credentials stored in the repository
* CLI never generates secrets automatically
* CLI never writes credentials to disk

---

# Versioning

This project follows **Semantic Versioning**.
```
v0.x  → experimental development
v1.x  → stable production releases
```

---

# License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.