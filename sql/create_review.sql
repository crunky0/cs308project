INSERT INTO ratings (userid, productid, rating, comment, approved)
VALUES (:userid, :productid, :rating, :comment, :approved)
RETURNING reviewid, userid, productid, rating, comment, approved;