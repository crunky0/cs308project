CREATE OR REPLACE FUNCTION update_average_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET averageRating = (
        SELECT COALESCE(ROUND(AVG(rating), 2), 0) -- Round to 2 decimal places, default to 0 if no ratings
        FROM ratings
        WHERE productID = NEW.productID
    )
    WHERE productID = NEW.productID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_product_average_rating
AFTER INSERT OR UPDATE ON ratings
FOR EACH ROW
EXECUTE FUNCTION update_average_rating();