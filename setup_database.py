# setup_database.py
import os
from dotenv import load_dotenv
import asyncpg #type: ignore
from asyncpg import Connection  # Import Connection type from asyncpg


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

async def run_sql_file(filename: str, connection: Connection) -> None:
    """Execute an SQL file on the given database connection."""
    with open(filename, 'r') as file:
        sql: str = file.read()  # Specify `sql` as a str type
        await connection.execute(sql)  # Execute the SQL command

async def setup_database() -> None:
    """Connect to the database and run setup SQL files."""
    conn: Connection = await asyncpg.connect(DATABASE_URL)  # Ensure `conn` is of type Connection
    
    await run_sql_file('sql/create_card_table.sql', conn)
    await run_sql_file('sql/insert_sample_data.sql', conn)
    await conn.close()  # Close the database connection

# Run setup
import asyncio
asyncio.run(setup_database())
