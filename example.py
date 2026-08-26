"""Example usage of sqlbrace. Requires a reachable SQL Server and the
Microsoft ODBC Driver for SQL Server installed on the host."""

from sqlbrace import SqlBrace, SqlBraceConfig

# Build config directly...
config = SqlBraceConfig(
    server="your-server.database.windows.net",
    database="your-database",
    username="your-username",
    password="your-password",
)

# ...or from environment variables (SQLBRACE_SERVER, SQLBRACE_DATABASE, etc.):
# config = SqlBraceConfig.from_env()

with SqlBrace(config) as db:
    rows = db.fetch_all("SELECT TOP 10 * FROM sys.tables")
    for row in rows:
        print(row)

    affected = db.execute_non_query(
        "UPDATE dbo.Widgets SET Status = ? WHERE Id = ?",
        ["active", 42],
    )
    print(f"{affected} row(s) updated")
