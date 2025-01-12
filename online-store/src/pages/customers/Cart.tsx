import React, { useEffect, useCallback , useRef} from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Navbar from '../../components/customer/layout/Navbar';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import './Cart.css';

const Cart = () => {
  const { user } = useAuth();
  const userId = user?.userid;
  const { cart, total, fetchCart, updateQuantity, removeFromCart } = useCart();
  const navigate = useNavigate();
  const location = useLocation();

  

  const fetchCartData = useCallback(() => {
    fetchCart(userId);
  }, [fetchCart, userId]);
  useEffect(() => {
    console.log('userId:', userId);
  }, [userId]);
  

  // Trigger fetching only when userId changesr
  useEffect(() => {
    if (userId) {
        fetchCartData();
    }
}, [userId]);

  const handleSearch = (query: string) => {
    console.log('Search query:', query);
  };

  const handleCheckout = () => {
    if (!userId) {
      alert('Please log in to proceed to checkout.');
      return;
    }
    navigate('/checkout');
  };

  const handleDecreaseQuantity = (productid: number) => {
    if (userId) {
      updateQuantity(productid, false, userId); // Decrease quantity for logged-in users
    } else {
      updateQuantity(productid, false); // Decrease quantity for guests
    }
  };

  const handleIncreaseQuantity = (productid: number) => {
    if (userId) {
      updateQuantity(productid, true, userId); // Increase quantity for logged-in users
    } else {
      updateQuantity(productid, true); // Increase quantity for guests
    }
  };

  const handleRemoveItem = (productid: number) => {
    if (userId) {
      removeFromCart(productid, userId); // Remove item for logged-in users
    } else {
      removeFromCart(productid); // Remove item for guests
    }
  };

  return (
    <div className="cart-page">
      <Navbar onSearch={handleSearch} />
      <div className="cart-container">
        {cart.length === 0 ? (
          <div className="empty-cart">
            <h2>Your cart is empty</h2>
            <p>Add some items to your cart to see them here!</p>
          </div>
        ) : (
          <>
            <div className="cart-items">
              {cart.map(item => (
                <div key={item.productid} className="cart-item">
                  <img src={item.image} alt={item.productname} className="item-image" />
                  <div className="item-details">
                    <h3>{item.productname}</h3>
                    <p>Quantity: {item.quantity}</p>
                    <p>
                      Price: 
                      {item.discountprice ? (
                        <>
                          <span style={{ textDecoration: "line-through", color: "gray" }}>
                            ${item.price.toFixed(2)}
                          </span>{" "}
                          <span style={{ color: "green", fontWeight: "bold" }}>
                            ${item.discountprice.toFixed(2)}
                          </span>
                        </>
                      ) : (
                        <>${item.price.toFixed(2)}</>
                      )}
                    </p>
                  </div>
                  <div className="quantity-controls">
                    <button
                      onClick={() => handleDecreaseQuantity(item.productid)}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button onClick={() => handleIncreaseQuantity(item.productid)}>+</button>
                  </div>
                  <button className="remove-btn"
                   onClick={() => handleRemoveItem(item.productid)}>Remove</button>
                </div>
              ))}
            </div>
            <div className="cart-summary">
              <h2>Order Summary</h2>
              <p>Total: ${total.toFixed(2)}</p>
              <button className="checkout-btn"
               onClick={handleCheckout}>Proceed to Checkout</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;