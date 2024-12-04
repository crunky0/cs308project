SELECT 
    r.reviewid, 
    r.userid, 
    r.productid, 
    r.rating,
    CASE 
        WHEN r.approved = TRUE THEN r.comment 
        ELSE 'This comment has not approved by the manager.' 
    END AS comment,
    r.approved,
    u.name,
    u.surname
FROM ratings r
JOIN users u ON r.userid = u.userid
WHERE r.productid = :productid;
