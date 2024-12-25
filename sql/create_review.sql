INSERT INTO ratings (userid, productid, rating, comment, approved)
VALUES (:userid, :productid, :rating, :comment, :approved)
RETURNING reviewid, userid, productid, rating, comment, approved,
          (SELECT name FROM users WHERE users.userid = :userid) AS name,
          (SELECT surname FROM users WHERE users.userid = :userid) AS surname;
