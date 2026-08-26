from __future__ import annotations

import logging
from typing import Any, Iterable, Optional

import pyodbc

from .config import SqlBraceConfig
from .exceptions import SqlBraceConnectionError

logger = logging.getLogger(__name__)


class SqlBrace:
    """A thin, reusable wrapper around a pyodbc SQL Server connection."""

    def __init__(self, config: SqlBraceConfig):
        self.config = config
        self._conn: Optional[pyodbc.Connection] = None

    def _build_connection_string(self) -> str:
        parts = [
            f"DRIVER={{{self.config.driver}}}",
            f"SERVER={self.config.server}",
            f"DATABASE={self.config.database}",
        ]
        if self.config.trusted_connection:
            parts.append("Trusted_Connection=yes")
        else:
            parts.append(f"UID={self.config.username}")
            parts.append(f"PWD={self.config.password}")
        parts.append(f"Encrypt={'yes' if self.config.encrypt else 'no'}")
        parts.append(
            f"TrustServerCertificate={'yes' if self.config.trust_server_certificate else 'no'}"
        )
        parts.append(f"Connection Timeout={self.config.timeout}")
        return ";".join(parts)

    def connect(self) -> pyodbc.Connection:
        """Open the connection if it isn't already open, and return it."""
        if self._conn is None:
            try:
                self._conn = pyodbc.connect(self._build_connection_string())
            except pyodbc.Error as exc:
                raise SqlBraceConnectionError(
                    f"Could not connect to {self.config.server}/{self.config.database}: {exc}"
                ) from exc
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SqlBrace":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def execute(self, query: str, params: Optional[Iterable[Any]] = None) -> pyodbc.Cursor:
        """Run a query and return the open cursor. Caller is responsible for closing it."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        return cursor

    def fetch_all(self, query: str, params: Optional[Iterable[Any]] = None) -> list[dict]:
        """Run a SELECT and return rows as a list of dicts."""
        cursor = self.execute(query, params)
        try:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Optional[Iterable[Any]] = None) -> Optional[dict]:
        cursor = self.execute(query, params)
        try:
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        finally:
            cursor.close()

    def execute_non_query(self, query: str, params: Optional[Iterable[Any]] = None) -> int:
        """Run an INSERT/UPDATE/DELETE, commit, and return the affected row count."""
        cursor = self.execute(query, params)
        try:
            self._conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
