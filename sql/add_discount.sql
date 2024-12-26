UPDATE products
SET discountPrice = :discountPrice
WHERE productID = :productID
RETURNING *;