from unittest.mock import MagicMock, patch

import pytest

from sqlbrace import SqlBrace, SqlBraceConfig


def make_config(**overrides):
    defaults = dict(
        server="localhost",
        database="testdb",
        username="user",
        password="pass",
    )
    defaults.update(overrides)
    return SqlBraceConfig(**defaults)


def test_config_requires_credentials_unless_trusted():
    with pytest.raises(ValueError):
        SqlBraceConfig(server="localhost", database="testdb")

    # trusted connection doesn't need username/password
    config = SqlBraceConfig(server="localhost", database="testdb", trusted_connection=True)
    assert config.trusted_connection is True


def test_connection_string_includes_credentials():
    config = make_config()
    db = SqlBrace(config)
    conn_str = db._build_connection_string()
    assert "SERVER=localhost" in conn_str
    assert "DATABASE=testdb" in conn_str
    assert "UID=user" in conn_str
    assert "PWD=pass" in conn_str


def test_connection_string_uses_trusted_connection():
    config = make_config(trusted_connection=True, username=None, password=None)
    db = SqlBrace(config)
    conn_str = db._build_connection_string()
    assert "Trusted_Connection=yes" in conn_str
    assert "UID=" not in conn_str


@patch("sqlbrace.connection.pyodbc.connect")
def test_fetch_all_maps_rows_to_dicts(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.description = [("id",), ("name",)]
    mock_cursor.fetchall.return_value = [(1, "a"), (2, "b")]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    db = SqlBrace(make_config())
    rows = db.fetch_all("SELECT id, name FROM t")

    assert rows == [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    mock_cursor.close.assert_called_once()


@patch("sqlbrace.connection.pyodbc.connect")
def test_execute_non_query_commits_and_returns_rowcount(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 3
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    db = SqlBrace(make_config())
    affected = db.execute_non_query("UPDATE t SET x = 1")

    assert affected == 3
    mock_conn.commit.assert_called_once()


@patch("sqlbrace.connection.pyodbc.connect")
def test_context_manager_closes_connection(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    with SqlBrace(make_config()) as db:
        db.connect()

    mock_conn.close.assert_called_once()
