import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function Header({ isLoggedIn, onLogout }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <header style={headerStyle}>
      <h1 style={{ display: 'inline' }}>Online Store</h1>
      <nav style={navStyle}>
        <Link to="/">Home</Link> | 
        <Link to="/cart">Shopping Cart</Link>
      </nav>
      {!isLoggedIn ? (
        <Link to="/auth">
          <button style={authButtonStyle}>Login / Sign Up</button>
        </Link>
      ) : (
        <div style={accountStyle} onClick={toggleDropdown}>
          <span style={accountSymbol}>☰</span>
          {isDropdownOpen && (
            <div style={dropdownMenuStyle}>
              <Link to="/my-orders" style={dropdownItemStyle}>My Orders</Link>
              <button style={logoutButtonStyle} onClick={onLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      )}
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

const accountStyle = {
  position: 'relative',
  cursor: 'pointer',
};

const accountSymbol = {
  fontSize: '20px',
};

const dropdownMenuStyle = {
  position: 'absolute',
  right: 0,
  backgroundColor: 'white',
  color: 'black',
  border: '1px solid #ddd',
  borderRadius: '5px',
  boxShadow: '0px 4px 6px rgba(0,0,0,0.1)',
};

const dropdownItemStyle = {
  display: 'block',
  padding: '10px',
  textDecoration: 'none',
  color: 'black',
  cursor: 'pointer',
};

const logoutButtonStyle = {
  display: 'block',
  padding: '10px',
  border: 'none',
  backgroundColor: 'red',
  color: 'white',
  cursor: 'pointer',
  borderRadius: '5px',
  width: '100%',
  textAlign: 'left',
};

export default Header;
