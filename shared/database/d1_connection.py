"""
Cloudflare D1 database adapter.

This module provides a small SQLite-compatible connection/cursor
interface over the Cloudflare D1 REST API.

The goal is to allow the existing query modules to continue using:

    cursor.execute(sql, params)
    cursor.fetchone()
    cursor.fetchall()
    cursor.lastrowid

without knowing whether the database is SQLite or Cloudflare D1.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


# =========================================================
# D1 ERROR
# =========================================================


class D1Error(RuntimeError):
    """
    Raised when Cloudflare D1 returns an error.
    """

    pass


# =========================================================
# D1 ROW
# =========================================================


class D1Row(dict):
    """
    Row object compatible with the way the existing code accesses
    sqlite3.Row:

        row["id"]
        row["key"]

    It also supports normal dictionary behavior.
    """

    pass


# =========================================================
# D1 CURSOR
# =========================================================


class D1Cursor:

    def __init__(
        self,
        connection: "D1Connection",
    ):

        self.connection = connection

        self._rows = []

        self._index = 0

        self._last_row_id = None

        self._last_meta = {}

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        sql,
        parameters=None,
    ):
        """
        Execute one SQL statement against D1.

        Parameters are sent to D1 as bound parameters rather than
        interpolated into SQL.
        """

        if parameters is None:
            parameters = []

        elif isinstance(parameters, tuple):
            parameters = list(
                parameters
            )

        elif not isinstance(parameters, list):
            parameters = list(
                parameters
            )

        result = self.connection._query(
            sql=sql,
            parameters=parameters,
        )

        self._rows = result["rows"]

        self._index = 0

        self._last_meta = result["meta"]

        self._last_row_id = (
            self._last_meta.get(
                "last_row_id"
            )
        )

        return self

    # =====================================================
    # FETCH ONE
    # =====================================================

    def fetchone(self):

        if self._index >= len(
            self._rows
        ):

            return None

        row = self._rows[
            self._index
        ]

        self._index += 1

        return row

    # =====================================================
    # FETCH ALL
    # =====================================================

    def fetchall(self):

        rows = self._rows[
            self._index:
        ]

        self._index = len(
            self._rows
        )

        return rows

    # =====================================================
    # LAST ROW ID
    # =====================================================

    @property
    def lastrowid(self):

        return self._last_row_id

    # =====================================================
    # META
    # =====================================================

    @property
    def meta(self):

        return self._last_meta


# =========================================================
# D1 CONNECTION
# =========================================================


class D1Connection:

    API_BASE_URL = (
        "https://api.cloudflare.com/client/v4"
    )

    def __init__(
        self,
        account_id: str,
        database_id: str,
        api_token: str,
    ):

        if not account_id:

            raise ValueError(
                "Cloudflare account ID is required"
            )

        if not database_id:

            raise ValueError(
                "Cloudflare D1 database ID is required"
            )

        if not api_token:

            raise ValueError(
                "Cloudflare API token is required"
            )

        self.account_id = (
            account_id
        )

        self.database_id = (
            database_id
        )

        self.api_token = (
            api_token
        )

        self.closed = False

    # =====================================================
    # CURSOR
    # =====================================================

    def cursor(self):

        self._check_open()

        return D1Cursor(
            self
        )

    # =====================================================
    # QUERY
    # =====================================================

    def _query(
        self,
        sql,
        parameters=None,
    ):

        self._check_open()

        if parameters is None:
            parameters = []

        url = (
            f"{self.API_BASE_URL}"
            f"/accounts/"
            f"{self.account_id}"
            f"/d1/database/"
            f"{self.database_id}"
            f"/query"
        )

        payload = {
            "sql": sql,
            "params": parameters,
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(
                payload
            ).encode("utf-8"),
            headers={
                "Authorization": (
                    f"Bearer "
                    f"{self.api_token}"
                ),
                "Content-Type": (
                    "application/json"
                ),
                "Accept": (
                    "application/json"
                ),
            },
            method="POST",
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=30,
            ) as response:

                body = response.read()

        except urllib.error.HTTPError as error:

            body = error.read()

            message = (
                self._extract_error_message(
                    body
                )
            )

            raise D1Error(
                f"D1 HTTP error "
                f"{error.code}: "
                f"{message}"
            ) from error

        except urllib.error.URLError as error:

            raise D1Error(
                "Unable to connect to "
                f"Cloudflare D1: {error}"
            ) from error

        try:

            data = json.loads(
                body
            )

        except json.JSONDecodeError as error:

            raise D1Error(
                "Cloudflare returned invalid "
                "JSON"
            ) from error

        if not data.get(
            "success",
            False,
        ):

            raise D1Error(
                self._extract_api_errors(
                    data
                )
            )

        results = data.get(
            "result",
            []
        )

        if not results:

            return {
                "rows": [],
                "meta": {},
            }

        result = results[0]

        if not result.get(
            "success",
            False,
        ):

            raise D1Error(
                self._extract_api_errors(
                    result
                )
            )

        raw_rows = result.get(
            "results"
        )

        if raw_rows is None:

            rows = []

        else:

            rows = [
                D1Row(row)
                for row in raw_rows
            ]

        meta = result.get(
            "meta",
            {}
        )

        return {
            "rows": rows,
            "meta": meta,
        }

    # =====================================================
    # COMMIT
    # =====================================================

    def commit(self):
        """
        D1 queries are committed by the D1 service.

        This method exists to keep the same interface as
        SQLiteConnection.
        """

        self._check_open()

    # =====================================================
    # ROLLBACK
    # =====================================================

    def rollback(self):
        """
        D1 REST queries cannot provide a persistent SQLite
        transaction across independent HTTP requests.

        This is therefore intentionally a no-op.

        Important:
        code that requires atomic multi-statement transactions
        should eventually use D1's batch/transaction mechanism
        rather than relying on this method.
        """

        self._check_open()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.closed = True

    # =====================================================
    # CONTEXT MANAGER
    # =====================================================

    def __enter__(self):

        self._check_open()

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
    # INTERNAL
    # =====================================================

    def _check_open(self):

        if self.closed:

            raise D1Error(
                "D1 connection is closed"
            )

    @staticmethod
    def _extract_error_message(
        body,
    ):

        try:

            data = json.loads(
                body
            )

        except Exception:

            return body.decode(
                "utf-8",
                errors="replace",
            )

        return D1Connection._extract_api_errors(
            data
        )

    @staticmethod
    def _extract_api_errors(
        data,
    ):

        errors = data.get(
            "errors",
            []
        )

        if not errors:

            return (
                "Unknown Cloudflare D1 error"
            )

        messages = []

        for error in errors:

            if isinstance(
                error,
                dict,
            ):

                code = error.get(
                    "code"
                )

                message = error.get(
                    "message",
                    "Unknown error",
                )

                if code is not None:

                    messages.append(
                        f"[{code}] {message}"
                    )

                else:

                    messages.append(
                        str(message)
                    )

            else:

                messages.append(
                    str(error)
                )

        return "; ".join(
            messages
        )