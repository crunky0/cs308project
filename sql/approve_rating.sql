UPDATE ratings
SET approved = TRUE
WHERE reviewid = :reviewid
RETURNING reviewid, userid ,productid, rating, comment, approved;