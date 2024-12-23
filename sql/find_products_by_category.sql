SELECT productID, serialNumber, productName, productModel, description, distributerInfo, warranty, price, stock, categoryID, soldamount, discountPrice, image, averagerating
FROM products
WHERE categoryID = :categoryID;