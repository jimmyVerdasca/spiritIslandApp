from .sqlite_executor import SQLExecutor
from .d1_executor import D1Connection


class D1Executor(SQLExecutor):

    def __init__(
        self,
        connection: D1Connection,
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

        cursor.execute(
            sql,
            params,
        )

        return cursor

    def fetchone(
        self,
        sql,
        params=(),
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            sql,
            params,
        )

        return cursor.fetchone()

    def fetchall(
        self,
        sql,
        params=(),
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            sql,
            params,
        )

        return cursor.fetchall()

    # =====================================================
    # Transactions
    # =====================================================

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    # =====================================================
    # Lifecycle
    # =====================================================

    def close(self):

        self.connection.close()