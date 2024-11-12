SELECT 
    reviewID AS "reviewID", 
    userID AS "userID", 
    productID AS "productID", 
    review, 
    comment, 
    approved
FROM ratings
WHERE productID = :productID AND approved = TRUE;