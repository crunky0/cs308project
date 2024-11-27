from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models import Order, OrderItem, Product
from typing import Dict
from db import database  # Import the Database instance

class OrderService:
    def __init__(self, db):
        self.db = db

    async def create_order(self, order_data: Dict) -> Dict:
        """
        Creates an order, adds order items, and updates stock.

        Args:
            order_data (Dict): Data for creating the order, including user ID, total amount, and items.

        Returns:
            Dict: Confirmation message with the created order ID.

        Raises:
            ValueError: If stock is insufficient for any product.
            SQLAlchemyError: If there is a database error.
        """
        try:
            # Use the transaction() method for database transaction management
            async with self.db.transaction():
                # Insert the order
                query = """
                    INSERT INTO orders (userid, totalamount)
                    VALUES (:userid, :totalamount)
                    RETURNING orderid
                """
                values = {
                    "userid": order_data["userid"],
                    "totalamount": order_data["totalamount"]
                }
                result = await self.db.fetch_one(query, values)
                orderid = result["orderid"]

                # Process order items and update stock
                for item in order_data["items"]:
                    # Check stock
                    stock_query = "SELECT stock FROM products WHERE productid = :productid"
                    stock_result = await self.db.fetch_one(stock_query, {"productid": item["productid"]})
                    if not stock_result or stock_result["stock"] < item["quantity"]:
                        raise ValueError(f"Insufficient stock for product ID {item['productid']}")

                    # Update stock
                    update_stock_query = """
                        UPDATE products
                        SET stock = stock - :quantity
                        WHERE productid = :productid
                    """
                    await self.db.execute(update_stock_query, {
                        "quantity": item["quantity"],
                        "productid": item["productid"]
                    })

                    # Insert order item
                    insert_item_query = """
                        INSERT INTO order_items (orderid, productid, quantity, price)
                        VALUES (:orderid, :productid, :quantity, :price)
                    """
                    await self.db.execute(insert_item_query, {
                        "orderid": orderid,
                        "productid": item["productid"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    })

                return {"orderid": orderid, "message": "Order created successfully"}

        except ValueError as ve:
            raise ValueError(f"Stock issue: {str(ve)}")
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
