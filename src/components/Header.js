import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header style={headerStyle}>
      <h1 style={{ display: 'inline' }}>Online Store</h1>
      <nav style={navStyle}>
        <Link to="/">Home</Link> | 
        <Link to="/cart">Shopping Cart</Link>
      </nav>
      <Link to="/auth">
        <button style={authButtonStyle}>Sign Up / Login</button>
      </Link>
    </header>
  );
}

const headerStyle = {
  background: '#282c34',
  color: 'white',
  padding: '10px 20px',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
};

const navStyle = {
  flexGrow: 1,
  textAlign: 'center',
};

const authButtonStyle = {
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px 15px',
  borderRadius: '5px',
  cursor: 'pointer',
};

export default Header;
