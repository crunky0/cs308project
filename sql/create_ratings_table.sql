CREATE TABLE IF NOT EXISTS ratings (
    reviewID SERIAL PRIMARY KEY,
    userID INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    review DECIMAL(2, 1) CHECK (review >= 0.5 AND review <= 5.0),  -- Allows for values like 0.5, 1.0, ..., 5.0
    comment TEXT,
    approved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE, -- if a user is deleted it also deletes the reviews from the user
    FOREIGN KEY (productID) REFERENCES products(productID) ON DELETE CASCADE -- same as the user
);
