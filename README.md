# djangoplay-cli

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Lint](https://img.shields.io/badge/lint-ruff-informational)
![Formatting](https://img.shields.io/badge/format-ruff-informational)

**djangoplay-cli** provides a lightweight command-line interface for developers working on the **DjangoPlay ecosystem**.

The goal of this tool is to simplify common development tasks such as running the development server and managing Celery workers — without requiring complex local setup.

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

Clone the repository:

```bash
git clone https://github.com/binaryfleet/djangoplay-cli.git
cd djangoplay-cli
```

Install the CLI locally:

```bash
pip install -e .
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
