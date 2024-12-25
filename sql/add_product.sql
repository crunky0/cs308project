INSERT INTO products (serialNumber, productName, productModel, description, distributerInfo, warranty, price, cost, stock, categoryID, soldamount, discountPrice, image)
VALUES (:serialnumber, :productname, :productmodel, :description, :distributerinfo, :warranty, :price, :cost ,:stock, :categoryid, :soldamount, :discountprice, :image)
RETURNING *;