from db import database
import asyncio

async def update_users_table():
    
    # Alter table to add new columns
    alter_table_query = """
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS taxID VARCHAR(50),
    ADD COLUMN IF NOT EXISTS homeAddress VARCHAR(255),
    ADD COLUMN IF NOT EXISTS name VARCHAR(100),
    ADD COLUMN IF NOT EXISTS surname VARCHAR(100),
    ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE;
    """

    await database.connect()
    await database.execute(alter_table_query)
    await database.disconnect()

# Run the migration
if __name__ == "__main__":
    asyncio.run(update_users_table())
