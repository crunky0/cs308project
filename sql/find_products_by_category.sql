SELECT productID, serialNumber, productName, productModel, description, distributerInfo, warranty, price, stock, categoryID, soldamount, discountPrice, image
FROM products
WHERE categoryID = :categoryID;