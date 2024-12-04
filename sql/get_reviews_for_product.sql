SELECT 
    reviewid, 
    userid, 
    productid, 
    rating,
    comment, 
    approved
FROM ratings
WHERE productID = :productid AND approved = TRUE;