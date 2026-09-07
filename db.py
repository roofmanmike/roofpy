"""
Snowflake connection and table setup.
Security: credentials come only from environment variables.
"""

import os
from contextlib import contextmanager
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
import snowflake.connector
from snowflake.connector import DictCursor

# Load local development settings from .env without hard-coding credentials.
load_dotenv()

REQUIRED_ENV = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA",
]

def _validate_env():
    # Fail early with one actionable message when connection settings are incomplete.
    missing = [key for key in REQUIRED_ENV if not os.getenv(key)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Copy .env.example to .env and fill in the values."
        )
    if not os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH") and not os.getenv("SNOWFLAKE_PASSWORD"):
        raise EnvironmentError(
            "Set SNOWFLAKE_PRIVATE_KEY_PATH for key-pair authentication. "
            "SNOWFLAKE_PASSWORD is supported only as a temporary migration fallback."
        )

def _load_private_key():
    key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    if not key_path:
        return None

    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=(
                os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE") or ""
            ).encode("utf-8") or None,
        )

    return private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

@contextmanager
def get_connection():
    """Context manager that yields a Snowflake connection and closes it cleanly."""
    # Flow: validate settings, open the connection, yield it to the caller, then close it.
    _validate_env()
    connection_options = dict(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        client_session_keep_alive=True,
    )
    private_key = _load_private_key()
    if private_key:
        connection_options["private_key"] = private_key
    else:
        connection_options["password"] = os.getenv("SNOWFLAKE_PASSWORD")

    conn = snowflake.connector.connect(**connection_options)
    try:
        # Explicitly select the configured context before callers run unqualified SQL.
        with conn.cursor() as cur:
            cur.execute("USE DATABASE IDENTIFIER(%s)", (os.getenv("SNOWFLAKE_DATABASE"),))
            cur.execute("USE SCHEMA IDENTIFIER(%s)", (os.getenv("SNOWFLAKE_SCHEMA"),))
        yield conn
    finally:
        conn.close()

def create_users_table():
    """Create the users table if it does not already exist."""
    # Startup calls this once so later registration and login queries have a table to use.
    with get_connection() as conn:
        with conn.cursor() as cur:
            # IF NOT EXISTS makes startup safe to repeat without replacing existing data.
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id            INTEGER AUTOINCREMENT START 1 INCREMENT 1,
                    email         VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                    PRIMARY KEY (id),
                    UNIQUE (email)
                )
            """)
            print("✓ users table is ready")