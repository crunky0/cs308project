from db import database
import asyncio

async def apply_sql_commands():
    # Split the SQL into separate commands
    sql_commands = [
        """
        CREATE OR REPLACE FUNCTION update_average_rating()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE products
            SET averageRating = (
                SELECT COALESCE(ROUND(AVG(rating), 2), 0) -- Round to 2 decimal places, default to 0 if no ratings
                FROM ratings
                WHERE productID = NEW.productID
            )
            WHERE productID = NEW.productID;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """,
        """
        CREATE TRIGGER update_product_average_rating
        AFTER INSERT OR UPDATE ON ratings
        FOR EACH ROW
        EXECUTE FUNCTION update_average_rating();
        """
    ]

    await database.connect()
    try:
        # Execute each command sequentially
        for command in sql_commands:
            await database.execute(command)
            print("Executed command successfully.")
    except Exception as e:
        print(f"Error applying SQL changes: {e}")
    finally:
        await database.disconnect()

async def update_existing_average_ratings():
    update_query = """
        UPDATE products
        SET averageRating = COALESCE((
            SELECT ROUND(AVG(rating), 2)
            FROM ratings
            WHERE ratings.productID = products.productID
        ), 0);
    """
    await database.connect()
    try:
        await database.execute(update_query)
        print("Existing average ratings updated successfully.")
    except Exception as e:
        print(f"Error updating average ratings: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(apply_sql_commands())
    #asyncio.run(update_existing_average_ratings())
