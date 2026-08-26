class SqlBraceError(Exception):
    """Base exception for sqlbrace."""


class SqlBraceConnectionError(SqlBraceError):
    """Raised when a connection to SQL Server cannot be established."""
