CREATE TABLE IF NOT EXISTS order_items (
    orderItemID SERIAL PRIMARY KEY,
    orderID INT REFERENCES orders(orderID),
    productID INT REFERENCES products(productID),
    quantity INT,
    price NUMERIC(10,2)
);
