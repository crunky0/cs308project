SELECT * FROM products 
WHERE categoryID = (
    SELECT categoryID FROM categories
    WHERE name = :category_name
);