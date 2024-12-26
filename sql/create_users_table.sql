CREATE TABLE IF NOT EXISTS users (
    userID SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,           
    role VARCHAR(50) DEFAULT 'Customer',
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    taxID VARCHAR(50),
    homeAddress VARCHAR(255)
);
