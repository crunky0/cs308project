# db.py
import os
from databases import Database
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

# Create a Database instance
database = Database(DATABASE_URL)

# Dependency function to use the database in endpoints
async def get_db():
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()
