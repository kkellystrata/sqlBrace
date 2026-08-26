from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SqlBraceConfig:
    """Connection settings for a SQL Server instance."""

    server: str
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    driver: str = "ODBC Driver 18 for SQL Server"
    trusted_connection: bool = False
    encrypt: bool = True
    trust_server_certificate: bool = False
    timeout: int = 30

    def __post_init__(self) -> None:
        if not self.server:
            raise ValueError("server is required")
        if not self.database:
            raise ValueError("database is required")
        if not self.trusted_connection and not (self.username and self.password):
            raise ValueError(
                "username and password are required unless trusted_connection is True"
            )

    @classmethod
    def from_env(cls, prefix: str = "SQLBRACE_") -> "SqlBraceConfig":
        """Build config from environment variables, e.g. SQLBRACE_SERVER, SQLBRACE_DATABASE."""

        def env(name: str, default: Optional[str] = None) -> Optional[str]:
            return os.environ.get(f"{prefix}{name}", default)

        trusted = env("TRUSTED_CONNECTION", "false")
        encrypt = env("ENCRYPT", "true")
        trust_cert = env("TRUST_SERVER_CERTIFICATE", "false")

        return cls(
            server=env("SERVER", ""),
            database=env("DATABASE", ""),
            username=env("USERNAME"),
            password=env("PASSWORD"),
            driver=env("DRIVER", "ODBC Driver 18 for SQL Server"),
            trusted_connection=trusted.lower() in ("1", "true", "yes"),
            encrypt=encrypt.lower() in ("1", "true", "yes"),
            trust_server_certificate=trust_cert.lower() in ("1", "true", "yes"),
            timeout=int(env("TIMEOUT", "30")),
        )
