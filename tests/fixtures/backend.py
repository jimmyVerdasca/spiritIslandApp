import socket
import subprocess
import sys
import time

import pytest

from config.active import API_URL


def _parse_host_port(url: str):
    from urllib.parse import urlparse

    parsed = urlparse(url)

    if not parsed.hostname or not parsed.port:
        raise RuntimeError(f"Invalid API_URL: {url}")

    return parsed.hostname, parsed.port


def _wait_for_server(host, port, timeout=10):
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)

    raise RuntimeError(
        f"Backend did not start on {host}:{port}"
    )


@pytest.fixture(scope="session")
def backend_server():
    host, port = _parse_host_port(API_URL)

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            host,
            "--port",
            str(port),
        ]
    )

    try:
        _wait_for_server(host, port)
        yield
    finally:
        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()