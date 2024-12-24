import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import Navbar from '../../components/customer/layout/Navbar';
import './WishlistPage.css';

interface WishlistItem {
  productid: number;
  productname: string;
  price: number;
  image: string;
}

const WishlistPage: React.FC = () => {
  const { user } = useAuth();
  const { addToCart } = useCart();
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchWishlist = useCallback(async () => {
    if (!user) return;
    try {
      const response = await fetch(`http://localhost:8000/wishlist?userid=${user.userid}`);
      if (!response.ok) throw new Error('Failed to fetch wishlist');
      const data = await response.json();
      setWishlist(data.wishlist || []);
    } catch (error) {
      console.error('Error fetching wishlist:', error);
    } finally {
      setLoading(false);
    }
  }, [user]);

  const handleRemoveFromWishlist = async (productid: number) => {
    if (!user) return;
    try {
      const response = await fetch(
        `http://localhost:8000/wishlist/remove?userid=${user.userid}&productid=${productid}`,
        { method: 'DELETE' }
      );
      if (!response.ok) throw new Error('Failed to remove item from wishlist');
      setWishlist((prev) => prev.filter((item) => item.productid !== productid));
    } catch (error) {
      console.error('Error removing from wishlist:', error);
    }
  };

  const handleMoveToCart = async (productid: number) => {
    if (!user) return;
    try {
      await addToCart(productid, 1, user.userid);
      await handleRemoveFromWishlist(productid);
    } catch (error) {
      console.error('Error moving item to cart:', error);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, [fetchWishlist]);

  return (
    <div className="wishlist-page">
      <Navbar onSearch={(query) => console.log(query)} />
      <div className="wishlist-container">
        <h1 className="wishlist-title">Your Wishlist</h1>
        {loading ? (
          <p>Loading your wishlist...</p>
        ) : wishlist.length === 0 ? (
          <div className="empty-wishlist">
            <h2>Your wishlist is empty</h2>
            <p>Browse products and add them to your wishlist!</p>
          </div>
        ) : (
          <div className="wishlist-items">
            {wishlist.map((item) => (
              <div key={item.productid} className="wishlist-item">
                <img src={item.image} alt={item.productname} className="wishlist-item-image" />
                <div className="wishlist-item-details">
                  <h2>{item.productname}</h2>
                  <p>${item.price.toFixed(2)}</p>
                </div>
                <div className="wishlist-item-actions">
                  <button
                    className="move-to-cart-btn"
                    onClick={() => handleMoveToCart(item.productid)}
                  >
                    Move to Cart
                  </button>
                  <button
                    className="remove-btn"
                    onClick={() => handleRemoveFromWishlist(item.productid)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default WishlistPage;