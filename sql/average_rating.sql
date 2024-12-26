SELECT AVG(rating) AS average_rating
FROM ratings
WHERE productid = :productid;