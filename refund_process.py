from databases import Database
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List
from datetime import datetime, timedelta

class RefundService:
    def __init__(self, db: Database):
        self.db = db

    async def validate_order_for_refund(self, orderid: int) -> Dict:
        """
        Validate if the order is eligible for a refund.

        Args:
            orderid (int): ID of the order to validate.

        Returns:
            Dict: Order details if eligible.

        Raises:
            ValueError: If the order is not found or is ineligible for refund.
        """
        try:
            # Check if the order exists and fetch the order date
            query_order_date = """
                SELECT order_date, total_amount
                FROM orders
                WHERE orderid = :orderid
            """
            order_data = await self.db.fetch_one(query_order_date, {"orderid": orderid})

            if not order_data:
                raise ValueError("Order not found")

            # Check if the order is within the 30-day refund period
            max_refund_date = order_data["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            # Check delivery status
            query_delivery_status = """
                SELECT status
                FROM deliveries
                WHERE orderid = :orderid
            """
            delivery = await self.db.fetch_one(query_delivery_status, {"orderid": orderid})

            if delivery and delivery["status"] == "Completed":
                raise ValueError("Refund cannot be processed for completed deliveries")

            return order_data

        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund validation: {str(e)}")

    async def process_refund(self, orderid: int, product_quantities: List[Dict[str, int]]) -> float:
        """
        Process the refund for selected products by updating the order status and restoring stock.

        Args:
            orderid (int): ID of the order to refund.
            product_quantities (List[Dict[str, int]]): List of products with their quantities to refund.

        Returns:
            float: Total refunded amount for the selected products.

        Raises:
            ValueError: If the order is not found or refund is ineligible.
            Exception: If a database error occurs.
        """
        try:
            # Validate the order for refund
            await self.validate_order_for_refund(orderid)

            async with self.db.transaction():
                # Calculate the total refund amount for the selected products
                total_refunded_amount = 0.0

                for item in product_quantities:
                    productid = item["productid"]
                    quantity = item["quantity"]

                    # Fetch product price
                    query_product_price = """
                        SELECT price
                        FROM order_items
                        WHERE orderid = :orderid AND productid = :productid
                    """
                    product_data = await self.db.fetch_one(query_product_price, {
                        "orderid": orderid,
                        "productid": productid
                    })

                    if not product_data:
                        raise ValueError(f"Product ID {productid} not found in the order")

                    product_price = product_data["price"]
                    total_refunded_amount += product_price * quantity

                    # Restore stock for refunded items
                    restore_stock_query = """
                        UPDATE products
                        SET stock = stock + :quantity
                        WHERE productid = :productid
                    """
                    await self.db.execute(restore_stock_query, {
                        "quantity": quantity,
                        "productid": productid
                    })

                    # Update order items for refunded quantities
                    update_order_item_query = """
                        UPDATE order_items
                        SET quantity = quantity - :quantity
                        WHERE orderid = :orderid AND productid = :productid
                    """
                    await self.db.execute(update_order_item_query, {
                        "quantity": quantity,
                        "orderid": orderid,
                        "productid": productid
                    })

                # Update the order status to 'Partially Refunded' if some items remain
                # Otherwise, mark it as 'Refunded'
                query_remaining_items = """
                    SELECT COUNT(*) AS remaining_items
                    FROM order_items
                    WHERE orderid = :orderid AND quantity > 0
                """
                remaining_items = await self.db.fetch_one(query_remaining_items, {"orderid": orderid})

                if remaining_items["remaining_items"] > 0:
                    update_order_status_query = """
                        UPDATE orders
                        SET status = 'Partially Refunded'
                        WHERE orderid = :orderid
                    """
                else:
                    update_order_status_query = """
                        UPDATE orders
                        SET status = 'Refunded'
                        WHERE orderid = :orderid
                    """
                await self.db.execute(update_order_status_query, {"orderid": orderid})

                return total_refunded_amount

        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund processing: {str(e)}")
