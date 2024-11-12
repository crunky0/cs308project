INSERT INTO ratings (userID, productID, review, comment, approved)
VALUES (:userID, :productID, :review, :comment, :approved)
RETURNING reviewID AS "reviewID", userID AS "userID", productID AS "productID", review, comment, approved;