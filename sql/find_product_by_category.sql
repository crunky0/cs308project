SELECT * FROM products 
WHERE category_id = (
    SELECT category_id FROM categories
    WHERE name = :category_name
);