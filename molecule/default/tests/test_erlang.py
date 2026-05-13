"""Testinfra tests for anxs-erlang role."""


def test_erlang_base_package_installed(host):
    """Verify erlang-base package is installed."""
    assert host.package("erlang-base").is_installed


def test_erlang_crypto_package_installed(host):
    """Verify erlang-crypto is installed (representative package)."""
    assert host.package("erlang-crypto").is_installed


def test_erl_binary_exists(host):
    assert host.file("/usr/lib/erlang/bin/erl").exists


def test_erl_runs_and_reports_otp_version(host):
    cmd = host.run(
        "erl -eval 'io:format(\"~s\", [erlang:system_info(otp_release)]), halt().' -noshell"
    )
    assert cmd.rc == 0
    version = int(cmd.stdout.strip())
    assert version >= 26


def test_gpg_key_configured(host):
    """Verify the .sources file references a signing key."""
    f = host.file("/etc/apt/sources.list.d/rabbitmq-erlang.sources")
    content = f.content_string
    assert "Signed-By:" in content


def test_apt_repo_configured(host):
    f = host.file("/etc/apt/sources.list.d/rabbitmq-erlang.sources")
    assert f.exists
    assert f.is_file
    content = f.content_string
    assert "deb1.rabbitmq.com/rabbitmq-erlang" in content


def test_apt_pinning_configured(host):
    f = host.file("/etc/apt/preferences.d/erlang")
    assert f.exists
    content = f.content_string
    assert "Pin-Priority: 1000" in content
    assert "deb1.rabbitmq.com" in content


def test_rebar3_binary_exists(host):
    f = host.file("/usr/local/bin/rebar3")
    assert f.exists
    assert f.mode == 0o755


def test_rebar3_runs(host):
    cmd = host.run("rebar3 --version")
    assert cmd.rc == 0
    assert "rebar" in cmd.stdout.lower()


def test_epmd_dropin_exists(host):
    socket_dropin = host.file(
        "/etc/systemd/system/epmd.socket.d/anxs-erlang.conf"
    )
    service_dropin = host.file(
        "/etc/systemd/system/epmd.service.d/anxs-erlang.conf"
    )
    assert socket_dropin.exists or service_dropin.exists


def test_epmd_dropin_has_listen_address(host):
    socket_dropin = host.file(
        "/etc/systemd/system/epmd.socket.d/anxs-erlang.conf"
    )
    service_dropin = host.file(
        "/etc/systemd/system/epmd.service.d/anxs-erlang.conf"
    )
    if socket_dropin.exists:
        content = socket_dropin.content_string
    elif service_dropin.exists:
        content = service_dropin.content_string
    else:
        raise AssertionError("No EPMD drop-in found")
    assert "127.0.0.1" in content
    assert "4369" in content


def test_epmd_reachable(host):
    assert host.run("epmd -names").rc == 0


def test_epmd_port_listening(host):
    assert host.socket("tcp://127.0.0.1:4369").is_listening
