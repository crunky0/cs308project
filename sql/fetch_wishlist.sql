SELECT p.productid, p.productname, p.price, p.image, p.discountprice
FROM wishlist w
JOIN products p ON w.productid = p.productid
WHERE w.userid = :userid;