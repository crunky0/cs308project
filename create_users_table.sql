CREATE TABLE IF NOT EXISTS users (
    userID SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,           
    role VARCHAR(50) DEFAULT 'Customer'       
);
