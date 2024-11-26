from db import database
import asyncio

async def update_products_table():
    
    # Alter table to add new columns
    alter_table_query = """
    ALTER TABLE products
    ADD COLUMN IF NOT EXISTS soldAmount INT
    """

    await database.connect()
    await database.execute(alter_table_query)
    await database.disconnect()

# Run the migration
if __name__ == "__main__":
    asyncio.run(update_products_table())