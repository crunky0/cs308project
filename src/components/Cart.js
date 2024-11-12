import React from 'react';

function Cart({ cartItems }) {
  return (
    <div style={cartStyle}>
      <h1>Your Shopping Cart</h1>
      {cartItems.length > 0 ? (
        <ul style={cartListStyle}>
          {cartItems.map((item, index) => (
            <li key={index} style={cartItemStyle}>
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p><strong>Price:</strong> ${item.price}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Your cart is currently empty.</p>
      )}
    </div>
  );
}

const cartStyle = {
  textAlign: 'center',
  padding: '20px',
};

const cartListStyle = {
  listStyle: 'none',
  padding: 0,
};

const cartItemStyle = {
  marginBottom: '20px',
  borderBottom: '1px solid #ddd',
  paddingBottom: '10px',
};

export default Cart;
