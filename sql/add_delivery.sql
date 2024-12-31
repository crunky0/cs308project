INSERT INTO deliveries (
    orderid,
    customerid,
    productid,
    quantity,
    total_price,
    delivery_address,
    status,
    orderdate,
    price
)
SELECT
    o.orderid,
    o.userid AS customerid,
    oi.productid,
    oi.quantity,
    o.totalamount AS total_price,
    u.homeaddress AS delivery_address,
    o.status AS status,
    o.orderdate AS orderdate,
    oi.price AS price
FROM order_items oi
JOIN orders o ON oi.orderid = o.orderid
JOIN users u ON o.userid = u.userid
WHERE o.orderid = :oid
  AND NOT EXISTS (
      SELECT 1
      FROM deliveries d
      WHERE d.orderid = oi.orderid
        AND d.productid = oi.productid
  )
RETURNING *;
