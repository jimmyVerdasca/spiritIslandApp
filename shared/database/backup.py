from pathlib import Path
import sqlite3


def backup_database(
    db: sqlite3.Connection,
    database_path: Path
) -> Path:

    backup_path = database_path.with_suffix(
        database_path.suffix + ".backup"
    )

    backup_db = sqlite3.connect(
        backup_path
    )

    try:
        db.backup(
            backup_db
        )

    finally:
        backup_db.close()

    return backup_path