INSERT INTO deliveries (
    orderid,
    customerid,
    productid,
    quantity,
    total_price,
    delivery_address, 
    completed
)
SELECT
    o.orderid,
    o.userid AS customerid,
    oi.productid,
    oi.quantity,
    o.totalamount AS total_price,      -- or (oi.price * oi.quantity) if `oi.price` is per-item
    'Default Address' AS delivery_address,  -- or pull from a column in `orders` if you have it
    FALSE AS completed
FROM order_items oi
JOIN orders o ON oi.orderid = o.orderid;
