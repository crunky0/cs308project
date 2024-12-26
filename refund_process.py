from databases import Database
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List

class RefundService:
    def __init__(self, db: Database):
        self.db = db

    async def validate_order_for_refund(self, orderid: int) -> Dict:
        
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
        Validate if the order is eligible for a refund.
        
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
        try:
            # Fetch the order details
            query_order = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                SELECT orderid, total_amount
                FROM orders
                WHERE orderid = :orderid
            
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
            order = await self.db.fetch_one(query_order, {"orderid": orderid})

            if not order:
                raise ValueError("Order not found")

            # Check delivery status
            query_delivery_status = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                SELECT status
                FROM deliveries
                WHERE orderid = :orderid
            
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
            delivery = await self.db.fetch_one(query_delivery_status, {"orderid": orderid})

            if delivery and delivery["status"] == "Completed":
                raise ValueError("Refund cannot be processed for completed deliveries")

            return order
        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund validation: {str(e)}")

    async def process_refund(self, orderid: int) -> float:
        
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
        Process the refund by updating the order status and restoring stock.
        
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
        try:
            async with self.db.transaction():
                # Update order status
                update_order_query = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                    UPDATE orders
                    SET status = 'Refunded'
                    WHERE orderid = :orderid
                
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                await self.db.execute(update_order_query, {"orderid": orderid})

                # Restore stock for refunded items
                query_order_items = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                    SELECT productid, quantity
                    FROM order_items
                    WHERE orderid = :orderid
                
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                order_items = await self.db.fetch_all(query_order_items, {"orderid": orderid})

                for item in order_items:
                    restore_stock_query = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                        UPDATE products
                        SET stock = stock + :quantity
                        WHERE productid = :productid
                    
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                    await self.db.execute(restore_stock_query, {
                        "quantity": item["quantity"],
                        "productid": item["productid"]
                    })

                # Return the total refunded amount
                query_total_amount = 
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                    SELECT total_amount
                    FROM orders
                    WHERE orderid = :orderid
                
            # Check if the order is within the 30-day refund period
            query_order_date = """
                SELECT order_date
                FROM orders
                WHERE orderid = :orderid
            """
            order_date = await self.db.fetch_one(query_order_date, {"orderid": orderid})
            if not order_date:
                raise ValueError("Order date not found")

            max_refund_date = order_date["order_date"] + timedelta(days=30)
            if datetime.now() > max_refund_date:
                raise ValueError("Refund request exceeds the 30-day period")

            
                total_amount = await self.db.fetch_one(query_total_amount, {"orderid": orderid})
                return total_amount["total_amount"]

        except SQLAlchemyError as e:
            raise Exception(f"Database error during refund processing: {str(e)}")

