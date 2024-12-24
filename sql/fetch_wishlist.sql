SELECT p.productid, p.productname, p.price, p.image
FROM wishlist w
JOIN products p ON w.productid = p.productid
WHERE w.userid = :userid;