# sqlBrace

A lightweight Python connector for Microsoft SQL Server, built on `pyodbc`.

## Requirements

- Python 3.9+
- The Microsoft ODBC Driver for SQL Server installed on the host (e.g. "ODBC Driver 18 for SQL Server")

## Install

```bash
pip install -r requirements.txt
```

## Usage

```python
from sqlbrace import SqlBrace, SqlBraceConfig

config = SqlBraceConfig(
    server="your-server.database.windows.net",
    database="your-database",
    username="your-username",
    password="your-password",
)

with SqlBrace(config) as db:
    rows = db.fetch_all("SELECT TOP 10 * FROM sys.tables")
    for row in rows:
        print(row)
```

Config can also be loaded from environment variables (see `.env.example`):

```python
config = SqlBraceConfig.from_env()
```

Set `SQLBRACE_TRUSTED_CONNECTION=true` (or `trusted_connection=True`) to use
Windows Authentication instead of a username/password.

## Queries

- `db.fetch_all(query, params)` — returns a list of dicts
- `db.fetch_one(query, params)` — returns a single dict or `None`
- `db.execute_non_query(query, params)` — for INSERT/UPDATE/DELETE, commits and returns the affected row count

Always pass values via `params` (a list/tuple of `?` placeholders) rather than
string-formatting them into the query, to avoid SQL injection.

## Tests

```bash
pip install pytest
pytest
```

Tests mock `pyodbc`, so no live SQL Server connection is required.
