--Category Model Table
CREATE TABLE IF NOT EXISTS categories(
    categoryID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
-- Product Model Table
CREATE TABLE IF NOT EXISTS products (
    productID SERIAL PRIMARY KEY,
    serialNumber SERIAL UNIQUE,
    productName VARCHAR(50)  NOT NULL,
    productModel VARCHAR(50)  NOT NULL,
    description VARCHAR(255)  NOT NULL,
    distributerInfo VARCHAR(255)  NOT NULL,
    warranty VARCHAR(50) NOT NULL,          
    price NUMERIC(10,2) NOT NULL CHECK (price > 0),
    stock INT NOT NULL CHECK (stock >=0 ),
    categoryID INT NOT NULL REFERENCES categories(categoryID)
);