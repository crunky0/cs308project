import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import './ProductCard.css';

// Define props for the ProductCard component
interface ProductCardProps {
  productid: number;
  productname: string;
  price: number;
  discountedPrice?: number; // Optional field
  image: string;
  description?: string; // Optional field
  averageRating?: number; // Optional field
  onClick?: () => void; // Optional field for custom click handler
}

const ProductCard: React.FC<ProductCardProps> = ({
  productid: id,
  productname: name,
  price,
  discountedPrice,
  image,
  description,
  averageRating,
  onClick,
}) => {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { user } = useAuth(); // Retrieve the logged-in user

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent the card click event from firing
    if (user) {
      // Add to cart for logged-in users
      addToCart(id, 1, user.userid); // Pass product ID, quantity, and user ID
    } else {
      // Add to cart for guests
      addToCart(id, 1); // Only pass product ID and quantity
    }
  };  

  return (
    <div className="product-card" onClick={onClick || (() => navigate(`/product/${id}`))}>
      <img src={image} alt={name} className="product-image" />
      <div className="product-info">
        <h3>{name}</h3>
        {description && <p className="description">{description}</p>}
        {averageRating !== undefined && averageRating !== null ? (
  <div className="rating">
    <span className="stars">
      {
        Array.from({ length: 5 }).map((_, index) => {
          const fullStarThreshold = index + 1;
          const halfStarThreshold = index + 0.5;
          if (averageRating >= fullStarThreshold) {
            return <span key={index} className="star full">★</span>; // Tam yıldız
          } else if (averageRating >= halfStarThreshold) {
            return <span key={index} className="star half">★</span>; // Yarım yıldız
          } else {
            return <span key={index} className="star empty">☆</span>; // Boş yıldız
          }
        })
      }
    </span>
    <span className="rating-count">{averageRating.toFixed(1)}/5</span>
  </div>
) : (
  <div className="rating">
    <span className="stars">
      {'☆'.repeat(5)}
    </span>
    <span className="rating-count">0/5</span>
  </div>
)}


        <div className="product-footer">
          <div className="price">
            {discountedPrice ? (
              <>
                <span className="original-price">${price.toFixed(2)}</span>
                <span className="discounted-price">${discountedPrice.toFixed(2)}</span>
              </>
            ) : (
              <span>${price.toFixed(2)}</span>
            )}
          </div>
          <button className="add-to-cart-btn" onClick={handleAddToCart}>
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
