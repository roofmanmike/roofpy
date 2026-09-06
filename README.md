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
