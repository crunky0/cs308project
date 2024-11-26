SELECT AVG(review) AS average_rating
FROM ratings
WHERE productID = :productID;