import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import React, { useState } from 'react';
import './ProductCard.css';

// Define props for the ProductCard component
interface ProductCardProps {
  productid: number;
  productname: string;
  price: number;
  discountedPrice?: number; // Optional field
  image: string;
  description?: string;
  stock: number; // Optional field
  averagerating: number; // Optional field
  onClick?: () => void; // Optional field for custom click handler
}

const ProductCard: React.FC<ProductCardProps> = ({
  productid: id,
  productname: name,
  price,
  discountedPrice,
  image,
  description,
  stock,
  averagerating,
  onClick,
}) => {
  const navigate = useNavigate();
  const { addToCart, cart } = useCart();
  const { user } = useAuth(); // Retrieve the logged-in user
  const [isInWishlist, setIsInWishlist] = useState(false);

  // Get the current quantity of the product in the cart
  const currentCartItem = cart.find((item) => item.productid === id);
  const currentQuantity = currentCartItem?.quantity || 0;

  // Disable the button if stock is 0 or if the cart already has the max available stock
  const isOutOfStock = stock === 0 || currentQuantity >= stock;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent the card click event from firing
    if (!isOutOfStock) {
      if (user) {
        // Add to cart for logged-in users
        addToCart(id, 1, user.userid); // Pass product ID, quantity, and user ID
      } else {
        // Add to cart for guests
        addToCart(id, 1); // Only pass product ID and quantity
      }
    }
  };


  const handleWishlistToggle = async (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent the card click event from firing
    if (!user) {
      alert('Please log in to manage your wishlist.');
      return;
    }

    try {
      if (isInWishlist) {
        // Remove from wishlist
        const response = await fetch(
          `http://localhost:8000/wishlist/remove?userid=${user.userid}&productid=${id}`,
          { method: 'DELETE' }
        );
        if (!response.ok) throw new Error('Failed to remove from wishlist');
        setIsInWishlist(false);
      } else {
        // Add to wishlist
        const response = await fetch('http://localhost:8000/wishlist/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid: user.userid, productid: id }),
        });
        if (!response.ok) throw new Error('Failed to add to wishlist');
        setIsInWishlist(true);
      }
    } catch (error) {
      console.error('Error managing wishlist:', error);
    }
  };

  return (
    <div className="product-card" onClick={onClick || (() => navigate(`/product/${id}`))}>
      <div
        className={`wishlist-button ${isInWishlist ? 'in-wishlist' : ''}`}
        onClick={handleWishlistToggle}
      >
        {isInWishlist ? '♥' : '♡'}
      </div>
      <img src={image} alt={name} className="product-image" />
      <div className="product-info">
        <h3>{name}</h3>
        {description && <p className="description">{description}</p>}
        {stock !== undefined && stock !== null && (
          <p className="stock">Stock: {stock}</p>
        )}
        {averagerating !== undefined && averagerating !== null ? (
          <div className="rating">
            <span className="stars">
              {Array.from({ length: 5 }).map((_, index) => {
                const fullStarThreshold = index + 1;
                const halfStarThreshold = index + 0.5;
                if (averagerating >= fullStarThreshold) {
                  return <span key={index} className="star full">★</span>; // Full star
                } else if (averagerating >= halfStarThreshold) {
                  return <span key={index} className="star half">★</span>; // Half star
                } else {
                  return <span key={index} className="star empty">★</span>; // Empty star
                }
              })}
            </span>
            <span className="rating-count">
              {Number.isInteger(averagerating) 
                ? averagerating 
                : averagerating.toFixed(1)
              }/5
            </span>
          </div>
        ) : (
          <div className="rating">
            <span className="stars">{'★'.repeat(5)}</span>
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
          <button 
            className={`add-to-cart-btn ${isOutOfStock ? 'disabled' : ''}`} 
            onClick={handleAddToCart} 
            disabled={isOutOfStock}
          >
            {isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;

