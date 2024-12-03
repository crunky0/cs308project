DELETE FROM products
WHERE productID = :productID
RETURNING *;