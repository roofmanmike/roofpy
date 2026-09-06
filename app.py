"""
roofpy – Data Engineering / Data Analyst Capstone
Simple secure user registration & login using Snowflake.
"""

from db import create_users_table
from auth import register, login

def main():
    print("=== roofpy (Snowflake) ===")
    print("Setting up database...")
    create_users_table()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            register(email, password)
        elif choice == "2":
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            login(email, password)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()