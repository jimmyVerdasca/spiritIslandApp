from pathlib import Path
import sqlite3

from shared.database.config import DATABASE_VERSION
from shared.database.backup import backup_database

from .migration_002 import upgrade as upgrade_002



MIGRATIONS = {
    2: upgrade_002,
}


def get_database_version(cursor):

    cursor.execute(
        "PRAGMA user_version"
    )

    return cursor.fetchone()[0]

def set_database_version(
    cursor,
    version
):

    cursor.execute(
        f"PRAGMA user_version = {version}"
    )


def run_migrations(database_path):
    
    db = sqlite3.connect(
        database_path
    )

    try:

        cursor = db.cursor()

        current_version = (
            get_database_version(
                cursor
            )
        )

        if current_version > DATABASE_VERSION:

            raise RuntimeError(
                "Database version is newer "
                "than the application version"
            )

        # DB backup creation as migration will be run right after
        if current_version < DATABASE_VERSION:
    
            backup_path = backup_database(
                db,
                Path(database_path)
            )

            print(
                f"Database backup created: "
                f"{backup_path}"
            )

        db.execute("BEGIN IMMEDIATE")
        next_version = current_version
        started_version = current_version
        while current_version < DATABASE_VERSION:
            
            next_version +=  1

            migration = MIGRATIONS.get(
                next_version
            )

            if migration is None:

                raise RuntimeError(
                    f"No migration found "
                    f"for version "
                    f"{next_version}"
                )

            print(
                f"Migrating database "
                f"from version "
                f"{current_version} "
                f"to version "
                f"{next_version}"
            )

            migration(
                cursor
            )

            set_database_version(
                cursor,
                next_version
            )

            current_version = (
                next_version
            )

        db.commit()
        print(
            f"Database migration completed: "
            f"version {started_version} -> {next_version}"
        )

    except Exception:

        print(
            "Database migration failed. "
            "Transaction rolled back."
        )
        db.rollback()

        raise

    finally:

        db.close()