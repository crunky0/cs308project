CREATE TABLE refund_requests (
    refundid SERIAL PRIMARY KEY,
    orderid INT NOT NULL,
    productid INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE,
    FOREIGN KEY (productid) REFERENCES products(productid) ON DELETE CASCADE
);