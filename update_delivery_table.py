from db import database
import asyncio

async def update_database_schema():
    # Connect to the database
    await database.connect()

    try:
        # Add the columns without NOT NULL constraint
        add_columns_query = """
        ALTER TABLE deliveries
            ADD COLUMN IF NOT EXISTS status TEXT,
            ADD COLUMN IF NOT EXISTS orderdate DATE;
        """

        # Populate the new columns using data from the orders table
        populate_columns_query = """
        UPDATE deliveries
        SET 
            status = orders.status,
            orderdate = orders.orderdate
        FROM orders
        WHERE deliveries.orderid = orders.orderid;
        """

        # Add the NOT NULL constraints
        add_constraints_query = """
        ALTER TABLE deliveries
            ALTER COLUMN status SET NOT NULL,
            ALTER COLUMN orderdate SET NOT NULL;
        """

        # Add a CHECK constraint on the status column
        add_check_constraint_query = """
        ALTER TABLE deliveries
            ADD CONSTRAINT check_status_valid
            CHECK (status IN ('processing', 'in-transit', 'delivered'));
        """

        drop_completed_column_query = """
        ALTER TABLE deliveries
            DROP COLUMN IF EXISTS completed;
        """

        update_delivery_address_query = """
        UPDATE deliveries
        SET 
            delivery_address = users.homeaddress
        FROM users
        WHERE deliveries.customerid = users.userid;
        """
         # Add a price column
        add_price_column_query = """
        ALTER TABLE deliveries
            ADD COLUMN IF NOT EXISTS price NUMERIC(10, 2);
        """

        # Populate the price column using data from the order_items table
        populate_price_query = """
        UPDATE deliveries
        SET 
            price = order_items.price
        FROM order_items
        WHERE deliveries.orderid = order_items.orderid
          AND deliveries.productid = order_items.productid;
        """

        # Add the NOT NULL constraint to the price column
        add_price_not_null_constraint_query = """
        ALTER TABLE deliveries
            ALTER COLUMN price SET NOT NULL;
        """

        # Execute the queries
        async with database.transaction():
            #await database.execute(add_columns_query)
            #await database.execute(populate_columns_query)
            #await database.execute(add_constraints_query)
            #await database.execute(add_check_constraint_query)
            #await database.execute(drop_completed_column_query)
            #await database.execute(update_delivery_address_query)
            await database.execute(add_price_column_query)
            await database.execute(populate_price_query)
            await database.execute(add_price_not_null_constraint_query)

        print("Database schema updated successfully!")

    finally:
        # Disconnect from the database
        await database.disconnect()

# Main entry point for the script
if __name__ == "__main__":
    asyncio.run(update_database_schema())