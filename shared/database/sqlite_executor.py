from .sqlite_connection import SQLiteConnection
from .executor import SQLExecutor


class SQLiteExecutor(SQLExecutor):

    def __init__(
        self,
        connection: SQLiteConnection,
    ):

        self.connection = connection

    # =====================================================
    # Queries
    # =====================================================

    def execute(
        self,
        sql,
        params=(),
    ):

        cursor = self.connection.cursor()

        try:

            cursor.execute(
                sql,
                params,
            )

            return cursor.rowcount

        finally:

            cursor.close()

    def fetchone(
        self,
        sql,
        params=(),
    ):

        cursor = self.connection.cursor()

        try:

            cursor.execute(
                sql,
                params,
            )

            return cursor.fetchone()

        finally:

            cursor.close()

    def fetchall(
        self,
        sql,
        params=(),
    ):

        cursor = self.connection.cursor()

        try:

            cursor.execute(
                sql,
                params,
            )

            return cursor.fetchall()

        finally:

            cursor.close()

    # =====================================================
    # Transactions
    # =====================================================

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    # =====================================================
    # Connection
    # =====================================================

    def close(self):

        self.connection.close()