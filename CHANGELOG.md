# Changelog

All notable changes to the **djangoplay-cli** developer tooling will be documented here.

This project follows **Semantic Versioning**.

---

## [1.0.3] - 2026-03-22

**Tag:** `v1.0.3-cross-platform-ssl-trust`

### SSL Certificate Management — Complete Cross-Platform Support

### Added

* `dplay dev certs` — new command to regenerate SSL certificates on demand
  from current `~/.dplay/config.yaml` without restarting the server
* `_trust_certificate_linux()` — trusts generated certificate in the Linux
  system store via `update-ca-certificates` (Debian, Ubuntu, derivatives)
* `_trust_certificate_wsl()` — detects WSL via `/proc/version` and trusts
  the certificate in both the Linux store and the Windows certificate store
  via `certutil.exe` so Chrome and Edge on the Windows host accept it
* `subdomains.extra_domains` support in `~/.dplay/config.yaml` — explicit
  subdomain SANs for Chrome which does not honour `*.localhost` wildcards
* `DNS:*.localhost` wildcard SAN added unconditionally for Firefox and Safari

### Fixed

* `cert_has_san()` — SAN entries now compared individually to avoid false
  mismatch caused by OpenSSL comma-space formatting vs `_build_san()` output;
  previously caused certificates to regenerate on every `dplay dev ssl` run
* `_build_san()` — fixed `sudomains` typo in config key lookup causing
  `extra_domains` to be silently ignored

### Changed

* `ensure_ssl_certificates()` — trust dispatch now covers macOS, Linux, and
  WSL in sequence; each handler is a no-op on non-matching platforms
* `certs_command()` — certificate paths printed as `~/.dplay/ssl/` relative
  paths instead of absolute user paths


## [1.0.2] - 2026-03-16

**Tag:** `v1.0.2-full-dev-environment-orchestration`
### 🚀 Major Release — DjangoPlay Developer Environment Manager

This release marks the first **production-ready release** of `djangoplay-cli`.

The CLI now functions as a full **local development environment manager**
for the DjangoPlay ecosystem. This release delivers a complete, automated local development startup sequence that mirrors the behaviour of hand-crafted shell scripts — without any shell configuration required.

### Added

* `utils/env_manager.py` — invokes host application `encrypt_env.py` as a subprocess
* `utils/redis_manager.py` — flushes Redis via `redis-cli` subprocess
* `utils/static_manager.py` — runs `manage.py collectstatic` via subprocess
* `utils/ssl_manager.py` — self-signed TLS certificate generation under `~/.dplay/ssl/`
* `utils/browser.py` — opens the application URL in the system default browser
* `utils/dev_startup.py` — environment summary display
* automatic macOS Keychain trust for generated SSL certificates
* graceful `TLSError` with user-friendly message: `TLS certificate unavailable. Use dplay dev http`
* `core/process_manager.py` — `restart_celery()`, `wait_for_celery()`, `stop_django()`
* clean session handover message when a new `dplay dev` session replaces a running server


### Changed

* `dplay dev ssl` — full startup orchestration: encrypt → flush Redis → static → SSL → Celery → browser → server
* `dplay dev http` — full startup orchestration: encrypt → flush Redis → static → Celery → browser → server
* `dplay dev` with no subcommand now defaults to `dplay dev http`
* `dplay dev worker` — runs with correct `cwd` and `DJANGO_SETTINGS_MODULE` from config
* `core/process_manager.py` — Celery launched via `python -m celery` using venv Python
* `utils/dev_startup.py` — reduced to `print_environment()` only; all other concerns separated
* `dplay dev up` and `dplay dev down` removed — superseded by `dplay dev http` and `dplay dev ssl`

### Architecture

* CLI remains fully decoupled from the host application — no Django imports
* host application is invoked exclusively via subprocess
* each utility owns a single concern following single-responsibility principle

---

## [1.0.0] - 2026-03-15

**Tag:** v1.0.0-dev-environment-manager

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