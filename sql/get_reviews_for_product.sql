SELECT 
    reviewid, 
    userid, 
    productid, 
    rating,
    CASE 
        WHEN approved = TRUE THEN comment 
        ELSE 'This comment has not approved by the manager.' 
    END AS comment,
    approved
FROM ratings
WHERE productid = :productid;
