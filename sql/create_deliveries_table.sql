CREATE TABLE IF NOT EXISTS deliveries (
    deliveryid      SERIAL PRIMARY KEY,
    orderid         INT NOT NULL REFERENCES orders(orderid),
    customerid      INT NOT NULL REFERENCES users(userid),
    productid       INT NOT NULL REFERENCES products(productid),
    quantity        INT NOT NULL,
    total_price     NUMERIC(10,2) NOT NULL,
    delivery_address TEXT NOT NULL,
    completed       BOOLEAN NOT NULL DEFAULT FALSE
);
