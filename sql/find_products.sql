SELECT * FROM products
WHERE (name IS NULL OR productname LIKE :name)
  AND (description IS NULL OR description LIKE :description)
  AND (model IS NULL OR productmodel LIKE :model);
