from db import database
import asyncio

async def update_database_schema():
    # Connect to the database
    await database.connect()

    try:
        # Queries to modify the `products` table
        modify_price_query = """
        ALTER TABLE products
        ALTER COLUMN price SET DEFAULT 1;
        """

        modify_cost_query = """
        ALTER TABLE products
        ALTER COLUMN cost SET DEFAULT 1;
        """

        modify_soldamount_query = """
        ALTER TABLE products
        ALTER COLUMN soldamount SET DEFAULT 0;
        """

        # Execute the queries in a transaction
        async with database.transaction():
            await database.execute(modify_price_query)
            await database.execute(modify_cost_query)

        print("Products table schema updated successfully!")

    finally:
        # Disconnect from the database
        await database.disconnect()

# Main entry point for the script
if __name__ == "__main__":
    asyncio.run(update_database_schema())