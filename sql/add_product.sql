INSERT INTO products (serialNumber, productName, productModel, description, distributerInfo, warranty, price, cost, stock, categoryID, soldamount, discountPrice, image)
VALUES (:serialNumber, :productName, :productModel, :description, :distributerInfo, :warranty, :price, :cost ,:stock, :categoryID, :soldamount, :discountPrice, :image)
RETURNING *;