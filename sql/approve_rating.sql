UPDATE ratings
SET approved = TRUE
WHERE reviewID = :reviewID
RETURNING reviewID AS "reviewID", userID AS "userID", productID AS "productID", review, comment, approved;