"""
roofpy – Data Engineering / Data Analyst Capstone
Simple secure user registration & login using Snowflake.
"""

from getpass import getpass

from db import create_users_table
from auth import register, login

def main():
    # Application flow: initialize the database before accepting user actions.
    print("=== roofpy (Snowflake) ===")
    print("Setting up database...")
    create_users_table()

    # Keep the CLI running until the user selects the exit option.
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Registration validates the input, hashes the password, and stores the user.
            email = input("Email: ").strip()
            password = getpass("Password: ")
            register(email, password)
        elif choice == "2":
            # Login loads the matching user and compares the supplied password hash.
            email = input("Email: ").strip()
            password = getpass("Password: ")
            login(email, password)
        elif choice == "3":
            # Breaking the loop ends the program cleanly.
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()