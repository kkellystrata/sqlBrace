# sqlBrace

Connects to SQL Server and lists the table names.

## Requirements

- Python 3.9+
- The Microsoft ODBC Driver for SQL Server installed on the host (e.g. "ODBC Driver 18 for SQL Server")

## Install

```bash
pip install -r requirements.txt
```

## Usage

```python
from sqlbrace import get_table_names

tables = get_table_names(
    server="your-server.database.windows.net",
    database="your-database",
    username="your-username",
    password="your-password",
)
print(tables)
```

Omit `username`/`password` to connect with Windows Authentication instead.

Or run it directly, reading settings from a `.env` file:

```bash
cp .env.example .env   # then fill in your values
python sqlbrace.py
```

If you see `SSL Provider: The certificate chain was issued by an authority
that is not trusted`, the server's certificate isn't CA-signed (common for
local/dev instances). Pass `trust_server_certificate=True`, or set
`SQLBRACE_TRUST_SERVER_CERTIFICATE=true` in `.env`.
