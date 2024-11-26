INSERT INTO orders (user_id, total_amount)
VALUES (:user_id, :total_amount)
RETURNING order_id;
