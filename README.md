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

The CLI is intentionally designed to remain:

* **Simple**
* **Predictable**
* **Portable**
* **Secure**
* **Developer-friendly**

---

# Philosophy

This project follows several guiding principles:

* **Minimal configuration**
* **No secrets in the repository**
* **Clear command structure**
* **Stable developer experience**
* **Incremental releases**
* **Developer-first ergonomics**

The CLI should help developers focus on building applications instead of managing local environment complexity.

---

# Supported Platforms

| Platform       | Support   |
| -------------- | --------- |
| macOS          | Supported |
| Linux          | Supported |
| Ubuntu         | Supported |
| Windows (WSL)  | Supported |
| Windows native | Limited   |

---

# Installation

Install from PyPI:

```bash
pip install djangoplay-cli
```

After installation, the CLI command becomes available globally:

```bash
dplay
```

---

# Basic Usage

Run the Django development server:

```bash
dplay dev http
```

Run the development server with HTTPS:

```bash
dplay dev ssl
```

Run the Celery worker:

```bash
dplay dev worker
```

---

# CLI Help

All commands provide detailed help:

```bash
dplay --help
```

Example:

```bash
dplay dev --help
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

scripts/
config/
docs/
tests/
```

The codebase separates:

| Layer        | Responsibility         |
| ------------ | ---------------------- |
| CLI Commands | User-facing commands   |
| Core         | Infrastructure logic   |
| Environment  | Environment validation |
| Utils        | Shared helpers         |

This structure ensures the project remains maintainable as the CLI grows.

---

# Development

Install development dependencies:

```bash
pip install -e .
pip install ruff pytest
```

Run lint checks:

```bash
ruff check .
```

Run tests:

```bash
pytest
```

---

# Security Principles

This project follows strict security rules:

* No credentials stored in the repository
* Secrets must be stored locally
* CLI never writes secrets automatically

---

# License

This project is licensed under the **MIT [LICENSE](LICENSE)**.
