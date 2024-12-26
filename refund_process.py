from databases import Database
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List

class RefundService:
    def __init__(self, db: Database):
        self.db = db

    async def validate_order_for_refund(self, orderid: int) -> Dict:
        """
        Validate if the order is eligible for a refund.
        """
        try:
            # Fetch the order details
            query_order = """
                SELECT orderid, total_amount
                FROM orders
                WHERE orderid = :orderid
            """
            order = await self.db.fetch_one(query_order, {"orderid": orderid})

            if not order:
                raise ValueError("Order not found")

            # Check delivery status
            query_delivery_status = """
                SELECT status
                FROM deliveries
                WHERE orderid = :orderid
            """
            delivery = await self.db.fetch_one(query_delivery_status, {"orderid": orderid})

            if delivery and delivery["status"] == "Completed":
                raise ValueError("Refund cannot be processed for completed deliveries")

            return order
        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund validation: {str(e)}")

    async def process_refund(self, orderid: int) -> float:
        """
        Process the refund by updating the order status and restoring stock.
        """
        try:
            async with self.db.transaction():
                # Update order status
                update_order_query = """
                    UPDATE orders
                    SET status = 'Refunded'
                    WHERE orderid = :orderid
                """
                await self.db.execute(update_order_query, {"orderid": orderid})

                # Restore stock for refunded items
                query_order_items = """
                    SELECT productid, quantity
                    FROM order_items
                    WHERE orderid = :orderid
                """
                order_items = await self.db.fetch_all(query_order_items, {"orderid": orderid})

                for item in order_items:
                    restore_stock_query = """
                        UPDATE products
                        SET stock = stock + :quantity
                        WHERE productid = :productid
                    """
                    await self.db.execute(restore_stock_query, {
                        "quantity": item["quantity"],
                        "productid": item["productid"]
                    })

                # Return the total refunded amount
                query_total_amount = """
                    SELECT total_amount
                    FROM orders
                    WHERE orderid = :orderid
                """
                total_amount = await self.db.fetch_one(query_total_amount, {"orderid": orderid})
                return total_amount["total_amount"]

        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund processing: {str(e)}")

