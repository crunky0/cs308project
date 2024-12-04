SELECT 
    reviewid, 
    userid, 
    productid, 
    rating,
    CASE 
        WHEN approved = TRUE THEN comment 
        ELSE 'Not Approved' 
    END AS comment,
    approved
FROM ratings
WHERE productid = :productid;
