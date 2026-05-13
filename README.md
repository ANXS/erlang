## [ANXS](https://github.com/ANXS) - erlang

[![CI Status](https://img.shields.io/github/actions/workflow/status/anxs/erlang/ci.yml)](https://github.com/ANXS/erlang/actions/workflows/ci.yml)
[![Maintenance](https://img.shields.io/maintenance/yes/2026.svg)](https://github.com/ANXS/erlang)
[![Ansible Role](https://img.shields.io/ansible/role/d/anxs/erlang)](https://galaxy.ansible.com/ui/standalone/roles/ANXS/erlang/)
[![License](https://img.shields.io/github/license/ANXS/erlang)](https://github.com/ANXS/erlang/blob/master/LICENSE)

Ansible role for installing Erlang/OTP via the RabbitMQ team's apt packages. Manages EPMD lifecycle (socket or service mode with systemd drop-ins), optional rebar3 installation, and GPG key / apt pinning for the RabbitMQ Erlang repository.

## Requirements & Dependencies

* Ansible 2.15 or higher (ansible-core 2.15+ / Ansible 8+).
* Ubuntu 20.04+ or Debian 11+.

## Variables

A partial listing of commonly adjusted variables. See [`defaults/main.yml`](https://github.com/ANXS/erlang/blob/master/defaults/main.yml) for the full set.

* `erlang_version_major` (default `"27"`) — OTP major series for the package repository.
* `erlang_rebar` (default `false`) — install rebar3 build tool.
* `erlang_rebar_version` (default `"3.27.0"`) — rebar3 version to install.

### EPMD management

By default the role manages the host's EPMD lifecycle: it detects available systemd units (preferring `epmd.socket`, falling back to `epmd.service`), drops in an override pinning the listen address and port, enables and starts the unit, and verifies reachability via `epmd -names`.

* `erlang_epmd_managed` (default `true`) — opt out by setting to `false`.
* `erlang_epmd_unit_kind` (default `"socket"`) — preferred unit kind. `"service"` for always-on daemon.
* `erlang_epmd_listen_address` (default `"127.0.0.1"`) — bind address. Non-loopback requires the safety latch below.
* `erlang_epmd_port` (default `4369`) — listener port.
* `erlang_epmd_allow_remote` (default `false`) — safety latch. Must be `true` to permit a non-loopback bind address.

**Service mode note:** when `erlang_epmd_unit_kind: service`, the role masks `epmd.socket` to prevent port competition. Switching back to socket mode requires `systemctl unmask epmd.socket`.

## Testing

Tests use [Molecule](https://github.com/ansible/molecule) with Docker and [Testinfra](https://testinfra.readthedocs.io/). Run the full suite with `make test`, or target a specific platform (e.g. `make test-ubuntu2404`).

The test suite verifies Erlang package installation, OTP version, apt repository and pinning configuration, EPMD systemd drop-in and reachability, and rebar3 installation. Tests run across all supported Linux distributions.

## Note on AI Usage

This project has been developed with AI assistance. Contributions making use of AI generated content are welcome, however they _must_ be human reviewed prior to submission as pull requests, or issues. All contributors must be able to fully explain and defend any AI generated code, documentation, issues, or tests they submit. Contributions making use of AI must have this explicitly declared in the pull request or issue. This also applies to utilization of AI for reviewing of pull requests.

## Feedback, bug-reports, requests, ...

Are always [welcome](https://github.com/ANXS/erlang/issues)!
