"""
User registration and login logic.
Security:
- Passwords are hashed with bcrypt (never stored in plain text)
- All queries use parameterized statements (SQL injection safe)
- Generic error messages to avoid user enumeration
"""

import bcrypt
from snowflake.connector import DictCursor
from db import get_connection

SALT_ROUNDS = 12

def hash_password(plain_password: str) -> str:
    # Generate a unique salt and return a one-way bcrypt hash for storage.
    return bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt(rounds=SALT_ROUNDS)
    ).decode("utf-8")

def verify_password(plain_password: str, stored_hash: str) -> bool:
    # Bcrypt extracts the salt and cost from the stored hash before comparing.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )

def register(email: str, password: str) -> bool:
    # Normalize the email first so equivalent addresses are treated consistently.
    email = email.strip().lower()
    if not email or len(password) < 8:
        print("Error: valid email and password (min 8 characters) required.")
        return False

    # Hash the password before opening the database connection; plaintext is never stored.
    password_hash = hash_password(password)

    try:
        # The connection context manager closes the Snowflake connection when finished.
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check for an existing account before attempting the insert.
                cur.execute(
                    "SELECT id FROM users WHERE email = %s",
                    (email,)
                )
                if cur.fetchone():
                    print("Error: email already registered.")
                    return False

                # Parameter binding keeps user input separate from the SQL statement.
                cur.execute(
                    "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                    (email, password_hash)
                )
                print(f"✓ Registered successfully: {email}")
                return True
    except Exception as e:
            # Do not expose database or authentication details to the user.
        print("Error: registration failed. Please try again later.")
        # Optional: log the real error somewhere secure
        # print(f"DEBUG: {e}")
        return False

def login(email: str, password: str) -> bool:
    # Normalize the lookup key in the same way registration normalizes it.
    email = email.strip().lower()
    if not email or not password:
        print("Error: email and password required.")
        return False

    try:
        # Fetch only the account needed for this login attempt.
        with get_connection() as conn:
            with conn.cursor(DictCursor) as cur:
                cur.execute(
                    "SELECT id, email, password_hash FROM users WHERE email = %s",
                    (email,)
                )
                user = cur.fetchone()

                if not user:
                    print("Error: invalid credentials.")
                    return False

                # Snowflake returns unquoted column names in uppercase by default.
                stored_hash = user["PASSWORD_HASH"]
                # Compare the submitted password to the stored bcrypt hash.
                if verify_password(password, stored_hash):
                    print(f"✓ Login successful. Welcome {user['EMAIL']} (id={user['ID']})")
                    return True
                else:
                    print("Error: invalid credentials.")
                    return False
    except Exception:
        print("Error: login failed. Please try again later.")
        return False