import sqlite3
from pathlib import Path


class SQLiteConnection:

    def __init__(
        self,
        database_path,
        row_factory=True,
    ):
        self.database_path = Path(
            database_path
        )

        self._connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
        )

        if row_factory:
            self._connection.row_factory = (
                sqlite3.Row
            )

    # =====================================================
    # Cursor
    # =====================================================

    def cursor(self):
        return self._connection.cursor()

    # =====================================================
    # Transaction
    # =====================================================

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    # =====================================================
    # Connection lifecycle
    # =====================================================

    def close(self):
        self._connection.close()

    # =====================================================
    # Context manager
    # =====================================================

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

        self.close()

    # =====================================================
    # SQLite escape hatch
    #
    # Keep this private-ish. It is useful for SQLite-only
    # initialization/migration code, but normal database
    # operations should use cursor().
    # =====================================================

    @property
    def raw(self):
        return self._connection