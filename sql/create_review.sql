INSERT INTO ratings (userID, productID, review, comment, approved)
VALUES (:userID, :productID, :review, :comment, :approved)
RETURNING reviewID, userID, productID, review, comment, approved;