import pandas as pd
import asyncio
from db import database

async def update_products_table_from_csv(file_path):
    """
    Update the products table with data from a CSV file.
    Replace all image links with a placeholder URL.
    """
    # Load the CSV file into a DataFrame
    products_df = pd.read_csv(file_path)
    products_df.rename(columns={"amountSold": "soldamount"}, inplace=True)

    # Replace all image links with the placeholder URL
    placeholder_image = "https://via.placeholder.com/150"
    products_df['image'] = placeholder_image

    # SQL query to insert or update products
    query = """
    INSERT INTO products (productID, serialNumber, productName, productModel, description, distributerInfo, warranty, price, stock, categoryID, soldamount, discountPrice, image)
    VALUES (:productID, :serialNumber, :productName, :productModel, :description, :distributerInfo, :warranty, :price, :stock, :categoryID, :soldamount, :discountPrice, :image)
    ON CONFLICT (productID)
    DO UPDATE SET 
        serialNumber = EXCLUDED.serialNumber,
        productName = EXCLUDED.productName,
        productModel = EXCLUDED.productModel,
        description = EXCLUDED.description,
        distributerInfo = EXCLUDED.distributerInfo,
        warranty = EXCLUDED.warranty,
        price = EXCLUDED.price,
        stock = EXCLUDED.stock,
        categoryID = EXCLUDED.categoryID,
        soldamount = EXCLUDED.soldamount,
        discountPrice = EXCLUDED.discountPrice,
        image = EXCLUDED.image;
    """

    await database.connect()
    try:
        # Insert or update each row in the DataFrame
        for _, row in products_df.iterrows():
            await database.execute(query, row.to_dict())
        print("Products table updated successfully.")
    except Exception as e:
        print(f"Error updating products table: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    # Path to the CSV file
    file_path = "realistic_products_with_images (3).csv"
    
    # Run the update script
    asyncio.run(update_products_table_from_csv(file_path))
