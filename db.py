import os
from databases import Database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the database connection instance
DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
