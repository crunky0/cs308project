SELECT * 
FROM products
WHERE description ILIKE '%' || :description || '%';