# Changelog

All notable changes to the **djangoplay-cli** developer tooling will be documented here.

This project follows **Semantic Versioning**.

---

## [0.1.0] - 2026-03-09

**Tag:** `v0.1.0-cli-foundation`

### 🚀 Initial CLI Foundation

This release introduces the first version of **djangoplay-cli**, a lightweight developer CLI for managing DjangoPlay development workflows.

The goal of this release is to establish the **core command structure and project architecture** that future releases will expand upon.

### Added

* Typer-based CLI framework for `dplay`
* command group `dplay dev`
* development server command `dplay dev http`
* HTTPS development server command `dplay dev ssl`
* Celery worker command `dplay dev worker`
* DjangoPlay repository detection using `git rev-parse`
* Python virtual environment validation
* automatic restart of Celery worker and beat processes
* shared startup helper for development commands
* consistent CLI startup output with environment summary
* service startup status display
* DRY architecture for dev command logic
* extensible project structure for future CLI commands

### Developer Experience

* clear CLI help output via Typer
* environment summary displayed when starting dev server
* automatic Celery restart to avoid duplicate workers
* unified startup behavior for HTTP and HTTPS modes

### Architecture

* production-ready CLI project structure
* separation of commands, core utilities, and environment checks
* extensible design for future command groups (`env`, `repo`, etc.)

---
