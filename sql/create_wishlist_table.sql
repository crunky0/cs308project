CREATE TABLE IF NOT EXISTS wishlist (
    userid INT NOT NULL,
    productid INT NOT NULL,
    PRIMARY KEY (userid, productid)
);