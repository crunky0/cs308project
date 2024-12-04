from db import database
import asyncio

async def update_products_table():
    # Separate SQL commands into individual queries
    rename_user_id_query = "ALTER TABLE ratings RENAME COLUMN review TO rating;"

    #rename_product_id_query = "ALTER TABLE cart RENAME COLUMN product_id TO productid;"

    await database.connect()
    try:
        # Execute queries sequentially
        await database.execute(rename_user_id_query)
        #await database.execute(rename_product_id_query)
        print("Table columns renamed successfully.")
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        await database.disconnect()

# Run the migration
if __name__ == "__main__":
    asyncio.run(update_products_table())
