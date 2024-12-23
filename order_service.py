from sqlalchemy.exc import SQLAlchemyError
from databases import Database
from models import Order, OrderItem, Product
from typing import Dict
from datetime import datetime, timedelta

class OrderService:
    def __init__(self, db: Database):
        self.db = db

    async def create_order(self, order_data: Dict) -> Dict:
        try:
            async with self.db.transaction():
                # Insert the order
                query = """
                    INSERT INTO orders (userid, totalamount)
                    VALUES (:userid, :totalamount)
                    RETURNING orderid
                """
                values = {"userid": order_data["userid"], "totalamount": order_data["totalamount"]}
                result = await self.db.fetch_one(query, values)

                if not result or "orderid" not in result:
                    print(f"DEBUG: fetch_one returned {result}")
                    raise KeyError("'orderid' key missing from result")
                orderid = result["orderid"]

                # Process items
                for item in order_data["items"]:
                    stock_query = "SELECT stock FROM products WHERE productid = :productid"
                    stock_result = await self.db.fetch_one(stock_query, {"productid": item["productid"]})
                    if not stock_result or stock_result["stock"] < item["quantity"]:
                        raise ValueError(f"Insufficient stock for product ID {item['productid']}")

                    await self.db.execute("UPDATE products SET stock = stock - :quantity WHERE productid = :productid", {"quantity": item["quantity"], "productid": item["productid"]})

                    await self.db.execute("INSERT INTO order_items (orderid, productid, quantity, price) VALUES (:orderid, :productid, :quantity, :price)", {
                        "orderid": orderid,
                        "productid": item["productid"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    })

                return {"orderid": orderid, "message": "Order created successfully"}
        except Exception as e:
            raise Exception(f"Order creation error: {str(e)}")
    async def get_orders_for_user(self, userid: int):
        """
        Fetch all orders for a specific user along with product details, including images and order status.

        Args:
            userid (int): The user ID to fetch orders for.

        Returns:
            List[dict]: A list of orders with product details.
        """
        try:
            query = """
                SELECT
                    o.orderid,
                    o.userid,
                    o.totalamount,
                    o.status,
                    oi.productid,
                    p.productname,
                    p.image,
                    oi.quantity,
                    oi.price
                FROM orders o
                JOIN order_items oi ON o.orderid = oi.orderid
                JOIN products p ON oi.productid = p.productid
                WHERE o.userid = :userid
            """
            rows = await self.db.fetch_all(query, {"userid": userid})
            
            orders = {}
            for row in rows:
                orderid = row["orderid"]
                if orderid not in orders:
                    orders[orderid] = {
                        "orderid": orderid,
                        "userid": row["userid"],
                        "totalamount": row["totalamount"],
                        "status": row["status"],
                        "items": []
                    }
                orders[orderid]["items"].append({
                    "productid": row["productid"],
                    "productname": row["productname"],
                    "image": row["image"],
                    "quantity": row["quantity"],
                    "price": row["price"]
                })
            return list(orders.values())
        except SQLAlchemyError as e:
            raise Exception(f"Database error while fetching orders: {str(e)}")
