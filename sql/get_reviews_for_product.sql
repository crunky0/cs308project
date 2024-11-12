SELECT reviewID, userID, productID, review, comment, approved
FROM ratings
WHERE productID = :productID AND approved = TRUE;