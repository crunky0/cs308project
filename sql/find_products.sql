SELECT * FROM products
WHERE (:product_name = '' OR productname LIKE :product_name)
  AND (:description = '' OR description LIKE :description)
  AND (:product_model = '' OR productmodel LIKE :product_model);
