UPDATE products
SET stock = stock + :quantity
WHERE productid = :productid;

