# djangoplay-cli

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Lint](https://img.shields.io/badge/lint-ruff-informational)
![Formatting](https://img.shields.io/badge/format-ruff-informational)

**djangoplay-cli** is a developer command-line interface for managing local
development environments within the **DjangoPlay ecosystem**.

The CLI simplifies common developer workflows such as:

- starting the development server
- managing Celery workers
- validating environment dependencies
- resetting development services
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
````

Verify installation:

```bash
dplay --version
```

Example output:

```
1.0.0
```

---

# CLI Overview

The CLI is organized into command groups.

```
dplay
 ├── dev
 │    ├── http
 │    ├── ssl
 │    ├── worker
 │    ├── up
 │    └── down
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

### Start HTTP development server

```
dplay dev http
```

Starts:

* Celery worker
* Celery beat
* Django development server

Server URL:

```
http://localhost:3333
```

---

### Start HTTPS development server

```
dplay dev ssl
```

Uses `runserver_plus` when available.

Server URL:

```
https://localhost:9999
```

---

### Start Celery worker

```
dplay dev worker
```

Starts the Celery worker for the DjangoPlay application.

---

### Start full development environment

```
dplay dev up
```

Starts all development services including:

* Celery worker
* Celery beat
* Django development server

---

### Stop development services

```
dplay dev down
```

Stops running Celery processes and development services.

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

# Logs

Display development logs.

```
dplay logs
```

(Currently reserved for future improvements.)

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

| Layer        | Responsibility                   |
| ------------ | -------------------------------- |
| CLI Commands | user-facing commands             |
| Core         | repository and service detection |
| Environment  | environment validation           |
| Utils        | reusable helpers                 |

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
* secrets must remain in local environment files
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