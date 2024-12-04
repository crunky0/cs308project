from db import database
import asyncio

async def update_orders_table():
    # SQL commands to modify the `orders` table
    add_status_column_query = """
        ALTER TABLE orders
        ADD COLUMN status TEXT DEFAULT 'processing';
    """
    
    add_check_constraint_query = """
        ALTER TABLE orders
        ADD CONSTRAINT check_order_status
        CHECK (status IN ('processing', 'in-transit', 'delivered'));
    """
    
    update_existing_rows_query = """
        UPDATE orders
        SET status = 'processing'
        WHERE status IS NULL;
    """

    await database.connect()
    try:
        # Execute queries sequentially
        await database.execute(add_status_column_query)
        print("Status column added successfully.")
        
        await database.execute(add_check_constraint_query)
        print("Check constraint added successfully.")
        
        await database.execute(update_existing_rows_query)
        print("Existing rows updated with default status.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        await database.disconnect()

# Run the migration
if __name__ == "__main__":
    asyncio.run(update_orders_table())