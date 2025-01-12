CREATE TABLE IF NOT EXISTS deliveries (
    deliveryid       SERIAL PRIMARY KEY,
    orderid          INT NOT NULL REFERENCES orders(orderid),
    customerid       INT NOT NULL REFERENCES users(userid),
    productid        INT NOT NULL REFERENCES products(productid),
    quantity         INT NOT NULL,
    total_price      NUMERIC(10, 2) NOT NULL,
    delivery_address TEXT NOT NULL,
    status           TEXT NOT NULL CHECK (status IN ('processing', 'in-transit', 'delivered')),
    orderdate        DATE NOT NULL REFERENCES orders(orderdate),
    price            NUMERIC(10, 2) NOT NULL
);