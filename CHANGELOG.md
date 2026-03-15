# Changelog

All notable changes to the **djangoplay-cli** developer tooling will be documented here.

This project follows **Semantic Versioning**.

---
## [1.0.0] - 2026-03-15

**Tag:** v1.0.0-dev-environment-manager

### 🚀 Major Release — DjangoPlay Developer Environment Manager

This release marks the first **production-ready release** of `djangoplay-cli`.

The CLI now functions as a full **local development environment manager**
for the DjangoPlay ecosystem.

### Added

* repository awareness allowing CLI commands from any directory inside the repo
* service detection utilities for Redis, Postgres and Celery
* process management commands

Commands introduced

* `dplay dev up`
* `dplay dev down`
* `dplay logs`

### Improvements

* improved CLI help output
* global `--version / -v` option
* CLI version derived from installed package metadata
* improved command structure and Typer command grouping
* cleaner CLI entrypoint implementation

### Architecture

* improved modular CLI architecture
* separation of command, core, environment and utility layers
* production-ready CLI structure for future extensibility

### Developer Experience

* commands can run from any subdirectory of the repository
* safe service startup preventing duplicate Celery workers
* consistent environment diagnostics

---

## [0.2.0] - 2026-03-10

**Tag:** `v0.2.0-system-diagnostics`

### Environment Diagnostics

### Added

* `dplay system doctor`
* `dplay system reset`
* environment diagnostics module
* redis / postgres / celery environment checks

### Developer Experience

* environment health checks before starting services
* CLI utilities for resetting development environment

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
