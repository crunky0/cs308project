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
  discountprice?: number; // Optional field
  image: string;
  description?: string;
  stock: number; // Optional field
  averagerating: number; // Optional field
  isInWishlist: boolean; // Passed down from parent
  updateWishlist: (productid: number) => void; // Function to toggle wishlist
  onClick?: () => void; // Optional field for custom click handler
}

const ProductCard: React.FC<ProductCardProps> = ({
  productid: id,
  productname: name,
  price,
  discountprice,
  image,
  description,
  stock,
  averagerating,
  isInWishlist,
  updateWishlist,
  onClick,
}) => {
  const navigate = useNavigate();
  const { addToCart, cart } = useCart();
  const { user } = useAuth(); // Retrieve the logged-in user

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


  const handleWishlistToggle = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent the card click event from firing
    if (!user) {
      alert('Please log in to manage your wishlist.');
      return;
    }
    updateWishlist(id); // Call the parent's updateWishlist function
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
              const partialStarThreshold = index + 0.5;
        
              if (averagerating >= fullStarThreshold) {
                // Full star
                return <span key={index} className="star full">★</span>;
              } else if (averagerating > index && averagerating < fullStarThreshold) {
                // Partial star
                const fillPercentage = (averagerating - index) * 100; // Calculate percentage to fill
                return (
                  <span key={index} className="star partial">
                    <span
                      className="partial-fill"
                      style={{ width: `${fillPercentage}%` }}
                    >
                      ★
                    </span>
                    <span className="empty-fill">★</span>
                  </span>
                );
              } else {
                // Empty star
                return <span key={index} className="star empty">★</span>;
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
            {discountprice ? (
              <>
                <span className="original-price">${price.toFixed(2)}</span>
                <span className="discounted-price">${discountprice.toFixed(2)}</span>
              </>
            ) : (
              <span className="price">${price.toFixed(2)}</span>
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

