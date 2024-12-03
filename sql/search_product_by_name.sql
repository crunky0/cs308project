SELECT * 
FROM products
WHERE productName ILIKE '%' || :productName || '%';