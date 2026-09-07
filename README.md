# roofpy

**Data Engineering / Data Analyst Capstone Project – 2026**

Secure Python authentication service backed by **Snowflake**.

## Features (current)
- User registration
- User login
- Passwords hashed with bcrypt
- All credentials stored in environment variables
- Parameterized SQL (SQL injection safe)

## Tech Stack
- Python 3.10+
- Snowflake (cloud data platform)
- `snowflake-connector-python`
- `bcrypt`
- `python-dotenv`

## Setup

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Snowflake key-pair authentication before September 21, 2026:
   - Generate an RSA private key locally and keep it outside Git.
   - Register the matching public key on the Snowflake user with `ALTER USER`.
   - Set `SNOWFLAKE_PRIVATE_KEY_PATH` in `.env`.
   - Set `SNOWFLAKE_PRIVATE_KEY_PASSPHRASE` only when the private key is encrypted.

The connector temporarily supports `SNOWFLAKE_PASSWORD` as a migration fallback, but password-only sign-ins must be removed before Snowflake's enforcement date.
