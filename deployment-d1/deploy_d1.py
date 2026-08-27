#!/usr/bin/env python3

import importlib.util
import json
import os
import re
import sqlite3
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

MIGRATIONS_DIR = (
    ROOT
    / "shared"
    / "database"
    / "migrations"
)

INITIAL_VERSION = 1

D1_SCHEMA_TABLE = "__spirit_island_schema_version"


# ============================================================
# Cloudflare D1 API
# ============================================================

class D1Client:

    def __init__(self):
        self.account_id = os.environ.get(
            "CLOUDFLARE_ACCOUNT_ID"
        )

        self.api_token = os.environ.get(
            "CLOUDFLARE_API_TOKEN"
        )

        self.database_id = os.environ.get(
            "CLOUDFLARE_D1_DATABASE_ID"
        )

        missing = []

        if not self.account_id:
            missing.append("CLOUDFLARE_ACCOUNT_ID")

        if not self.api_token:
            missing.append("CLOUDFLARE_API_TOKEN")

        if not self.database_id:
            missing.append("CLOUDFLARE_D1_DATABASE_ID")

        if missing:
            raise RuntimeError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

        self.url = (
            "https://api.cloudflare.com/client/v4"
            f"/accounts/{self.account_id}"
            f"/d1/database/{self.database_id}"
            "/query"
        )

    def execute(self, sql, params=None):

        payload = {
            "sql": sql,
        }

        if params:
            payload["params"] = params

        body = json.dumps(payload).encode("utf-8")

        request = Request(
            self.url,
            data=body,
            headers={
                "Authorization": (
                    f"Bearer {self.api_token}"
                ),
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:

            with urlopen(request) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as exc:

            response_body = exc.read().decode(
                "utf-8",
                errors="replace",
            )

            raise RuntimeError(
                "Cloudflare D1 API request failed "
                f"with HTTP {exc.code}:\n"
                f"{response_body}"
            ) from exc

        except URLError as exc:

            raise RuntimeError(
                "Could not connect to Cloudflare D1 API: "
                f"{exc}"
            ) from exc

        if not result.get("success"):

            raise RuntimeError(
                "Cloudflare D1 query failed:\n"
                + json.dumps(
                    result.get("errors", result),
                    indent=2,
                )
            )

        return result

    def query_one(self, sql):

        result = self.execute(sql)

        results = result.get("result", [])

        if not results:
            return None

        rows = results[0].get("results", [])

        if not rows:
            return None

        return rows[0]


# ============================================================
# Migration discovery
# ============================================================

def discover_migrations():

    migrations = {}

    pattern = re.compile(
        r"^migration_(\d+)\.py$"
    )

    for path in sorted(MIGRATIONS_DIR.glob(
        "migration_*.py"
    )):

        match = pattern.match(path.name)

        if not match:
            continue

        version = int(match.group(1))

        migrations[version] = path

    return migrations


def load_upgrade(path):

    module_name = (
        "spirit_island_d1_migration_"
        + path.stem
    )

    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Could not load migration: {path}"
        )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    upgrade = getattr(
        module,
        "upgrade",
        None,
    )

    if upgrade is None:
        raise RuntimeError(
            f"Migration {path} does not define "
            "upgrade(cursor)"
        )

    return upgrade


# ============================================================
# Recording cursor
# ============================================================

class RecordingCursor:
    """
    Executes nothing.

    Instead, records SQL statements issued by the
    existing Python migration functions.

    This lets us reuse the existing migration files
    without maintaining separate D1 SQL migrations.
    """

    def __init__(self):
        self.statements = []

    def execute(self, sql, parameters=None):

        sql = sql.strip()

        if not sql:
            return self

        if parameters:
            raise RuntimeError(
                "Parameterized SQL is not currently supported "
                "by the D1 migration exporter.\n\n"
                f"SQL:\n{sql}\n\n"
                f"Parameters:\n{parameters}"
            )

        self.statements.append(sql)

        return self

    def executemany(self, sql, parameters):

        raise RuntimeError(
            "executemany() is not supported by the "
            "D1 migration exporter."
        )

    def executescript(self, sql):

        sql = sql.strip()

        if sql:
            self.statements.append(sql)

        return self

    def fetchone(self):

        raise RuntimeError(
            "fetchone() is not supported by the D1 "
            "migration exporter. Migrations must currently "
            "be expressible as SQL execute() calls."
        )

    def fetchall(self):

        raise RuntimeError(
            "fetchall() is not supported by the D1 "
            "migration exporter."
        )


# ============================================================
# Replay Python migrations
# ============================================================

def replay_migrations(
    database_path,
    starting_version,
    target_version,
):
    """
    Apply the existing Python migrations to a temporary
    SQLite database.

    This validates that the migrations themselves work and
    leaves us with the exact schema/data state that should
    exist in D1.
    """

    migrations = discover_migrations()

    connection = sqlite3.connect(
        database_path
    )

    try:

        cursor = connection.cursor()

        current_version = starting_version

        while current_version < target_version:

            next_version = current_version + 1

            migration_path = migrations.get(
                next_version
            )

            if migration_path is None:

                raise RuntimeError(
                    f"No migration found for version "
                    f"{next_version}"
                )

            print(
                f"Applying Python migration "
                f"{current_version} → {next_version}: "
                f"{migration_path.name}"
            )

            upgrade = load_upgrade(
                migration_path
            )

            upgrade(cursor)

            current_version = next_version

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ============================================================
# SQLite → SQL
# ============================================================

def sqlite_dump(database_path):

    connection = sqlite3.connect(
        database_path
    )

    try:

        statements = []

        for statement in connection.iterdump():

            statement = statement.strip()

            if not statement:
                continue

            upper = statement.upper()

            # Do not send SQLite dump transaction commands
            # to D1.
            if upper in (
                "BEGIN TRANSACTION;",
                "COMMIT;",
            ):
                continue

            # Do not attempt to recreate SQLite's internal
            # sqlite_sequence table.
            if (
                "SQLITE_SEQUENCE"
                in upper
            ):
                continue

            # PRAGMA statements are not needed for the
            # application schema.
            if upper.startswith("PRAGMA "):
                continue

            statements.append(statement)

        return statements

    finally:
        connection.close()


# ============================================================
# D1 schema-version table
# ============================================================

def ensure_schema_table(client):

    client.execute(
        f"""
        CREATE TABLE IF NOT EXISTS
        {D1_SCHEMA_TABLE} (
            version INTEGER NOT NULL
        )
        """
    )


def get_d1_version(client):

    row = client.query_one(
        f"""
        SELECT version
        FROM {D1_SCHEMA_TABLE}
        LIMIT 1
        """
    )

    if row is None:
        return None

    return int(row["version"])


def set_d1_version(client, version):

    client.execute(
        f"""
        DELETE FROM {D1_SCHEMA_TABLE};

        INSERT INTO {D1_SCHEMA_TABLE}(version)
        VALUES ({version});
        """
    )


# ============================================================
# Initial bootstrap
# ============================================================

def bootstrap_d1(
    client,
    database_path,
    target_version,
):
    """
    First deployment.

    The temporary SQLite database is generated using the
    project's real init_db.py implementation.

    We then replay the existing Python migrations and import
    the resulting database state into D1.
    """

    print("D1 database is empty.")
    print("Creating initial SQLite database...")

    # init_db.py normally sets user_version to the current
    # application version. For migration replay we explicitly
    # reset it to version 1.
    from shared.database.init_db import (
        create_database,
    )

    create_database(database_path)

    connection = sqlite3.connect(
        database_path
    )

    try:

        connection.execute(
            f"PRAGMA user_version = {INITIAL_VERSION}"
        )

        connection.commit()

    finally:
        connection.close()

    print(
        f"Reset temporary SQLite database to "
        f"version {INITIAL_VERSION}"
    )

    replay_migrations(
        database_path,
        INITIAL_VERSION,
        target_version,
    )

    print(
        "Exporting final SQLite database..."
    )

    statements = sqlite_dump(
        database_path
    )

    if not statements:
        raise RuntimeError(
            "SQLite export produced no SQL."
        )

    print(
        f"Generated {len(statements)} SQL statements."
    )

    # D1 starts empty, so the entire current database
    # can be imported as one batch.
    sql = "\n\n".join(statements)

    print(
        "Importing initial database into D1..."
    )

    client.execute(sql)

    ensure_schema_table(client)

    set_d1_version(
        client,
        target_version,
    )

    print(
        f"D1 bootstrap completed at version "
        f"{target_version}."
    )


# ============================================================
# Incremental migration
# ============================================================

def migrate_d1(
    client,
    current_version,
    target_version,
):
    migrations = discover_migrations()

    if current_version > target_version:

        raise RuntimeError(
            f"D1 database version "
            f"{current_version} is newer than "
            f"application version "
            f"{target_version}."
        )

    if current_version == target_version:

        print(
            f"D1 is already at version "
            f"{target_version}."
        )

        return

    for version in range(
        current_version + 1,
        target_version + 1,
    ):

        migration_path = migrations.get(
            version
        )

        if migration_path is None:

            raise RuntimeError(
                f"No migration found for version "
                f"{version}"
            )

        print(
            f"Generating D1 SQL for migration "
            f"{current_version} → {version}: "
            f"{migration_path.name}"
        )

        upgrade = load_upgrade(
            migration_path
        )

        recorder = RecordingCursor()

        upgrade(recorder)

        if not recorder.statements:

            print(
                f"Migration {version} produced no SQL."
            )

        else:

            sql = "\n\n".join(
                recorder.statements
            )

            print(
                "Executing migration SQL:"
            )

            print(sql)

            client.execute(sql)

        set_d1_version(
            client,
            version,
        )

        current_version = version

        print(
            f"D1 migrated to version {version}."
        )


# ============================================================
# Main
# ============================================================

def main():

    # Import here so the repository root is already available.
    from shared.database.config import (
        DATABASE_VERSION,
    )

    target_version = int(
        DATABASE_VERSION
    )

    print(
        "========================================"
    )

    print(
        "Spirit Island D1 deployment"
    )

    print(
        f"Target database version: "
        f"{target_version}"
    )

    print(
        "========================================"
    )

    client = D1Client()

    with tempfile.TemporaryDirectory(
        prefix="spirit-island-d1-"
    ) as temp_dir:

        database_path = (
            Path(temp_dir)
            / "spirit_island.db"
        )

        ensure_schema_table(client)

        current_version = get_d1_version(
            client
        )

        if current_version is None:

            bootstrap_d1(
                client,
                database_path,
                target_version,
            )

        else:

            print(
                f"Current D1 version: "
                f"{current_version}"
            )

            migrate_d1(
                client,
                current_version,
                target_version,
            )

    print(
        "D1 deployment completed successfully."
    )


if __name__ == "__main__":

    try:
        main()

    except Exception as exc:

        print(
            "\nD1 deployment FAILED:",
            file=sys.stderr,
        )

        print(
            str(exc),
            file=sys.stderr,
        )

        raise