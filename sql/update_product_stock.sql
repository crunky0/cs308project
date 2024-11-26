UPDATE products
SET stock = stock - :quantity
WHERE product_id = :product_id;
