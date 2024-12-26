CREATE TABLE IF NOT EXISTS cart (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    productid INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (productid) ON DELETE CASCADE
);