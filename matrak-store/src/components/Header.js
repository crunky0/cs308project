import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header({ isLoggedIn, onLogout, onSearch }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(searchQuery); // Pass the search query to the parent
  };

  return (
    <header style={headerStyle}>
      <h1 style={headerTitleStyle} onClick={() => navigate('/')}>
        Matrak Store
      </h1>
      <form onSubmit={handleSearch} style={searchBarStyle}>
        <input
          type="text"
          placeholder="Search for products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={searchInputStyle}
        />
        <button type="submit" style={searchButtonStyle}>
          Search
        </button>
      </form>
      <div style={actionButtonsStyle}>
        <Link to="/cart" style={cartButtonStyle}>
          🛒
        </Link>
        {!isLoggedIn ? (
          <Link to="/auth">
            <button style={authButtonStyle}>Login / Sign Up</button>
          </Link>
        ) : (
          <div style={accountStyle} onClick={toggleDropdown}>
            <span style={accountSymbol}>☰</span>
            {isDropdownOpen && (
              <div style={dropdownMenuStyle}>
                <Link to="/my-orders" style={dropdownItemStyle}>
                  My Orders
                </Link>
                <button style={logoutButtonStyle} onClick={onLogout}>
                  Logout
                </button>
              </div>
            )}
          </div>
        )}
      </div>
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

const headerTitleStyle = {
  cursor: 'pointer',
  fontSize: '24px',
  margin: '0',
};

const searchBarStyle = {
  flexGrow: 1,
  display: 'flex',
  justifyContent: 'center',
  margin: '0 20px',
};

const searchInputStyle = {
  padding: '5px 10px',
  fontSize: '16px',
  width: '250px',
  borderRadius: '5px 0 0 5px',
  border: '1px solid #ccc',
};

const searchButtonStyle = {
  padding: '5px 10px',
  fontSize: '16px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  borderRadius: '0 5px 5px 0',
  cursor: 'pointer',
};

const actionButtonsStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '15px',
};

const cartButtonStyle = {
  fontSize: '24px',
  textDecoration: 'none',
  color: 'white',
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
