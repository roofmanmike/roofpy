"""
Snowflake connection and table setup.
Security: credentials come only from environment variables.
"""

import os
from contextlib import contextmanager
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector import DictCursor

# Load local development settings from .env without hard-coding credentials.
load_dotenv()

REQUIRED_ENV = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
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

@contextmanager
def get_connection():
    """Context manager that yields a Snowflake connection and closes it cleanly."""
    # Flow: validate settings, open the connection, yield it to the caller, then close it.
    _validate_env()
    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        client_session_keep_alive=True,
    )
    try:
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