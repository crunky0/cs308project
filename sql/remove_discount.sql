UPDATE products
SET discountPrice = NULL
WHERE productID = :productID
RETURNING *;