import React from 'react';
import { useNavigate } from 'react-router-dom';

function Cart({ cartItems, isLoggedIn }) {
  const navigate = useNavigate();

  const handleCheckout = () => {
    if (!isLoggedIn) {
      alert('You must log in to proceed with the checkout.');
      navigate('/auth'); // Redirect to login page
    } else {
      alert('Proceeding to checkout...');
      // Add checkout logic here
    }
  };

  return (
    <div style={cartStyle}>
      <h1>Your Shopping Cart</h1>
      {cartItems.length > 0 ? (
        <ul>
          {cartItems.map((item, index) => (
            <li key={index}>
              {item.name} - ${item.price} (Qty: {item.quantity || 1})
            </li>
          ))}
        </ul>
      ) : (
        <p>Your cart is empty.</p>
      )}
      <button
        style={checkoutButtonStyle}
        onClick={handleCheckout}
        disabled={cartItems.length === 0}
      >
        Proceed to Checkout
      </button>
    </div>
  );
}

const cartStyle = {
  textAlign: 'center',
  padding: '20px',
};

const checkoutButtonStyle = {
  marginTop: '20px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  cursor: 'pointer',
  borderRadius: '5px',
};

export default Cart;
