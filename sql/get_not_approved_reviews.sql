SELECT 
    r.reviewid, 
    r.userid, 
    r.productid, 
    r.rating,
    r.comment,
    r.approved,
    u.name,
    u.surname
FROM ratings r
JOIN users u ON r.userid = u.userid
WHERE r.approved = FALSE;