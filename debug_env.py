import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

print("🔍 Checking environment variables:\n")

print(f"DB_HOST     = {os.getenv('DB_HOST')}")
print(f"DB_PORT     = {os.getenv('DB_PORT')}")
print(f"DB_USERNAME = {os.getenv('DB_USERNAME')}")

# Show only part of the password for safety
db_password = os.getenv('DB_PASSWORD')
if db_password:
    masked = db_password[:2] + "*" * (len(db_password) - 4) + db_password[-2:]
    print(f"DB_PASSWORD = {masked}")
else:
    print("DB_PASSWORD = (not found)")

print(f"DB_DATABASE = {os.getenv('DB_DATABASE')}")