# roofpy

**Secure Snowflake Backend & Data Engineering Foundation**  
Data Engineering / Data Analyst Capstone Project – 2026

Python application that demonstrates production-minded practices for building on Snowflake: secure authentication, parameterized SQL, modular architecture, and a clear path toward scalable data engineering and analytics workloads.

---

## Overview

`roofpy` is a clean, secure foundation for working with Snowflake.  
It currently implements user registration and login via a command-line interface, with all credentials and connections handled according to modern security best practices.

The project is intentionally designed so it can grow into a full data platform layer (ETL, dimensional modeling, analytical views, and reporting).

---

## Key Features

- **Secure Snowflake connectivity** using key-pair authentication
- **Password hashing** with bcrypt (never store plaintext)
- **Fully parameterized SQL** (SQL injection safe)
- **Environment-based configuration** (no secrets in code)
- **Modular architecture** (`db.py`, `auth.py`, `app.py`)
- Automatic table creation on startup
- Clear separation of concerns ready for extension

---

## Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Language           | Python 3.10+                        |
| Data Platform      | Snowflake                           |
| Connector          | snowflake-connector-python          |
| Security           | bcrypt, cryptography (key-pair)     |
| Configuration      | python-dotenv                       |
| Interface          | Command-line (Bash-friendly)        |

---

## Project Structure
