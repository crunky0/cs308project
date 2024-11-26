import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Path to your SQL file
sql_file_path = 'sql/create_order_table.sql'

# Correctly specify types for asyncpg usage
async def run_sql_file(sql_file: str) -> None:
    # Connect to the database asynchronously
    connection = await asyncpg.connect(DATABASE_URL)

    # Read the SQL file
    with open(sql_file, 'r') as file:
        sql_script = file.read()

    try:
        # Execute the SQL commands from the file
        await connection.execute(sql_script)
        print("SQL script executed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        await connection.close()

# Running the async function
if __name__ == "__main__":
    asyncio.run(run_sql_file(sql_file_path))
