from db import database
import asyncio

# Load SQL from file function
def load_sql_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()

async def create_wishlist_table():
    # Load the SQL command from the provided file
    create_table_sql = load_sql_file("sql/create_wishlist_table.sql")
    
    await database.connect()
    try:
        # Execute the SQL command to create the wishlist table
        await database.execute(create_table_sql)
        print("Wishlist table created successfully.")
    except Exception as e:
        print(f"Error creating wishlist table: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(create_wishlist_table())