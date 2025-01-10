from db import database
import asyncio

async def update_database_schema():
    # Connect to the database
    await database.connect()

    try:
        # Drop the existing CHECK constraint for `orders`
        drop_orders_constraint_query = """
        ALTER TABLE orders
        DROP CONSTRAINT IF EXISTS check_order_status;
        """

        # Add the updated CHECK constraint for `orders`
        add_orders_constraint_query = """
        ALTER TABLE orders
        ADD CONSTRAINT check_order_status
        CHECK (status IN ('processing', 'in-transit', 'delivered', 'refunded', 'partially refunded'));
        """

        # Drop the existing CHECK constraint for `deliveries`
        drop_deliveries_constraint_query = """
        ALTER TABLE deliveries
        DROP CONSTRAINT IF EXISTS check_status_valid;
        """

        # Add the updated CHECK constraint for `deliveries`
        add_deliveries_constraint_query = """
        ALTER TABLE deliveries
        ADD CONSTRAINT check_status_valid
        CHECK (status IN ('processing', 'in-transit', 'delivered', 'refunded', 'partially refunded'));
        """

        # Execute the queries in a transaction
        async with database.transaction():
            await database.execute(drop_orders_constraint_query)
            await database.execute(add_orders_constraint_query)
            await database.execute(drop_deliveries_constraint_query)
            await database.execute(add_deliveries_constraint_query)

        print("Database schema updated successfully!")

    finally:
        # Disconnect from the database
        await database.disconnect()

# Main entry point for the script
if __name__ == "__main__":
    asyncio.run(update_database_schema())