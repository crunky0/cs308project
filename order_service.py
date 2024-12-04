from sqlalchemy.exc import SQLAlchemyError
from databases import Database
from models import Order, OrderItem, Product
from typing import Dict

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
