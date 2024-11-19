CREATE TABLE IF NOT EXISTS card (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (productid) ON DELETE CASCADE
);
