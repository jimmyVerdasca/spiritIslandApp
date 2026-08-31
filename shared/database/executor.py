from abc import ABC, abstractmethod


class SQLExecutor(ABC):
    """
    Backend-independent contract for executing SQL.

    Implementations may use completely different mechanisms
    internally.

        SQLiteExecutor -> SQLiteConnection
        D1Executor     -> D1Connection

    Callers should only depend on this interface.
    """

    # =====================================================
    # Queries
    # =====================================================

    @abstractmethod
    def execute(
        self,
        sql: str,
        params=(),
    ):
        """
        Execute a SQL statement.

        Used for INSERT, UPDATE, DELETE, and other statements
        where no result rows are required.
        """
        raise NotImplementedError

    @abstractmethod
    def fetchone(
        self,
        sql: str,
        params=(),
    ):
        """
        Execute a SQL query and return one row.

        Returns None when no rows are found.
        """
        raise NotImplementedError

    @abstractmethod
    def fetchall(
        self,
        sql: str,
        params=(),
    ):
        """
        Execute a SQL query and return all rows.
        """
        raise NotImplementedError

    # =====================================================
    # Transactions
    # =====================================================

    @abstractmethod
    def commit(self):
        """
        Commit the current transaction.

        Backends without persistent transactions may
        implement this as a no-op.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        """
        Roll back the current transaction.

        Backends without persistent transactions may
        implement this as a no-op.
        """
        raise NotImplementedError

    # =====================================================
    # Lifecycle
    # =====================================================

    @abstractmethod
    def close(self):
        """
        Release resources owned by the executor.
        """
        raise NotImplementedError