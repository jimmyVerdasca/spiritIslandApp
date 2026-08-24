import socket
import subprocess
import sys
import time
import shutil
import os

import pytest

from config.active import MODE, API_URL
from shared.database.config import BUNDLED_DB_PATH


def _parse_host_port(url: str):
    """
    Extract host and port from an API URL such as
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)

    host = parsed.hostname
    port = parsed.port

    if not host or not port:
        raise RuntimeError(f"Invalid API_URL: {url}")

    return host, port


def _wait_for_server(host: str, port: int, timeout: float = 10.0):
    """
    Wait until something is accepting TCP connections.
    """
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)

    raise RuntimeError(
        f"Backend did not start on {host}:{port} within {timeout} seconds."
    )


@pytest.fixture(scope="session", autouse=True)
def backend_server():
    """
    Start the backend automatically when the application is configured
    in HTTP mode.

    In standalone mode, nothing is started.
    """
    if MODE != "http":
        yield
        return

    host, port = _parse_host_port(API_URL)

    # Bind the backend so it is reachable through the configured API_URL.
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            str(host),
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

@pytest.fixture(scope="session", autouse=True)
def reset_test_database():
    database_path = os.environ["SPIRIT_ISLAND_DB_PATH"]

    os.makedirs(
        os.path.dirname(database_path),
        exist_ok=True,
    )

    shutil.copy2(
        BUNDLED_DB_PATH,
        database_path,
    )

    yield