from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime,timezone

Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementing ID
    username = Column(String(50), unique=True, index=True)  # Username column (varchar(100))
    password = Column(String(255))  # Password column (varchar(255))
    role = Column(String(50))  # Role column (varchar(50))
    name = Column(String(100))  # Name column (varchar(100))
    surname = Column(String(100))  # Surname column (varchar(100))
    email = Column(String(100), unique=True)  # Email column (varchar(100), unique)
    taxid = Column(String(50))  # Tax ID column (varchar(50))
    homeaddress = Column(String(255))  # Home address column (varchar(255))

    # Relationship to orders (a user can have many orders)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

# Category Table
class Category(Base):
    __tablename__ = 'categories'

    categoryid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    # Relationship to products (a category can have many products)
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name={self.name})>"

# Product Table
class Product(Base):
    __tablename__ = 'products'

    productid = Column(Integer, primary_key=True, autoincrement=True)
    serialnumber = Column(Integer, unique=True)
    productname = Column(String(50), nullable=False)
    productmodel = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    distributerinfo = Column(String(255), nullable=False)
    warranty = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    categoryid = Column(Integer, ForeignKey('categories.categoryid'))

    # Relationship to categories (each product belongs to one category)
    category = relationship("Category", back_populates="products")

    # Relationship to order items (a product can appear in many orders)
    order_items = relationship("OrderItem", back_populates="product")

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('stock >= 0', name='check_stock_non_negative'),
    )

    def __repr__(self):
        return f"<Product(name={self.productname}, price={self.price}, stock={self.stock})>"

# Order Table
# In models.py - Update the Order model to include a relationship to invoices

class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.userid'), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    order_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship to users (an order belongs to a user)
    user = relationship("User", back_populates="orders")

    # Relationship to order items (an order can have many items)
    order_items = relationship("OrderItem", back_populates="order")

    # Relationship to invoices (an order can have many invoices)
    invoices = relationship("Invoice", back_populates="order")

    def __repr__(self):
        return f"<Order(order_id={self.orderid}, total_amount={self.total_amount})>"


# Order Item Table
class OrderItem(Base):
    __tablename__ = 'order_items'

    order_itemid = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer, ForeignKey('orders.orderid'), nullable=False)
    productid = Column(Integer, ForeignKey('products.productid'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    # Relationship to orders (an order item belongs to one order)
    order = relationship("Order", back_populates="order_items")

    # Relationship to products (an order item corresponds to a product)
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(order_id={self.orderid}, product_id={self.productid}, quantity={self.quantity})>"

# Review Table
class Review(Base):
    __tablename__ = 'reviews'

    reviewid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'), nullable=False)
    productid = Column(Integer, ForeignKey('products.productid'), nullable=False)
    review = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    approved = Column(Boolean, default=False)

    # Relationship to users (a review belongs to one user)
    user = relationship("User")

    # Relationship to products (a review belongs to one product)
    product = relationship("Product")

    def __repr__(self):
        return f"<Review(user_id={self.userid}, product_id={self.productid}, rating={self.review})>"
    
    # In models.py
class Invoice(Base):
    __tablename__ = 'invoices'

    invoiceid = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer, ForeignKey('orders.orderid'), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    invoice_date = Column(DateTime, default=datetime.now(timezone.utc))
    file_path = Column(String(255), nullable=False)

    # Relationship to orders
    order = relationship("Order", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice(invoice_number={self.invoice_number}, order_id={self.orderid})>"


# models.py (example addition at the bottom of the file)

class Delivery(Base):
    __tablename__ = 'deliveries'

    deliveryid = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer, ForeignKey('orders.orderid'), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship back to orders
    order = relationship("Order")

    def __repr__(self):
        return f"<Delivery(delivery_id={self.deliveryid}, orderid={self.orderid}, status={self.status})>"
