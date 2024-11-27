import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import './ProductCard.css';

interface ProductCardProps {
  id: number;
  name: string;
  price: number;
  discountedPrice?: number;
  image: string;
  description: string;
  rating: number;
  reviews: number;
  color: string;
  material: string;
  date: string;
  categoryId: number;
}

const ProductCard: React.FC<ProductCardProps> = ({
  id,
  name,
  price,
  discountedPrice,
  image,
  description,
  rating = 0,
  reviews = 0
}) => {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const renderStars = (rating: number) => {
    return "★".repeat(Math.floor(rating)) + "☆".repeat(5 - Math.floor(rating));
  };
  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent the card click event from firing
    addToCart({
      id,
      name,
      price,
      image,
      size: "Default" // You might want to handle this differently
    });
  };


  const handleClick = () => {
    navigate(`/product/${id}`);
  };

  const renderPrice = () => {
    if (discountedPrice) {
      return (
        <div className="price-container">
          <span className="original-price">${price}</span>
          <span className="discounted-price">${discountedPrice}</span>
        </div>
      );
    }
    return <span className="price">${price}</span>;
  };

  return (
    <div className="product-card" onClick={handleClick}>
      <div className="wishlist-button" onClick={(e) => e.stopPropagation()}>♡</div>
      <img src={image} alt={name} className="product-image" />
      <div className="product-info">
        <h3>{name}</h3>
        <p className="description">{description}</p>
        {rating > 0 && (
          <div className="rating">
            <span className="stars">{renderStars(rating)}</span>
            <span className="review-count">({reviews})</span>
          </div>
        )}
        <div className="product-footer">
          {renderPrice()}
          <button 
          className="add-to-cart-btn"
          onClick={handleAddToCart}
        >
          Add to Cart
        </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;