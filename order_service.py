from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models import Order, OrderItem, Product

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: dict):
        async with self.db.begin():  # Use async context for transaction management
            try:
                # Create the order instance
                order = Order(
                    user_id=order_data["user_id"],  # Using user_id instead of userid
                    total_amount=order_data["total_amount"]  # Using total_amount instead of totalamount
                )
                self.db.add(order)
                await self.db.flush()  # Flush to get the order ID without committing

                # Add order items and update product stock
                for item in order_data["items"]:
                    # Check if the product is in stock
                    result = await self.db.execute(select(Product).where(Product.productid == item["product_id"]))
                    product = result.scalars().first()

                    if product and product.stock >= item["quantity"]:
                        # Reduce the product stock
                        product.stock -= item["quantity"]

                        # Add the order item
                        order_item = OrderItem(
                            order_id=order.order_id,
                            product_id=item["product_id"],
                            quantity=item["quantity"],
                            price=item["price"]
                        )
                        self.db.add(order_item)
                    else:
                        raise ValueError(f"Not enough stock for product {item['product_id']}")

                await self.db.commit()  # Commit all changes if successful
                return {"order_id": order.order_id, "message": "Order created successfully"}

            except SQLAlchemyError as e:
                await self.db.rollback()
                raise Exception(f"Database error: {str(e)}")

            except Exception as e:
                await self.db.rollback()
                raise Exception(f"Error creating order: {str(e)}")
