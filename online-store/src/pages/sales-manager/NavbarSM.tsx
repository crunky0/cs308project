import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './NavbarSM.css';

const NavbarPM: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/products');
  };

  return (
    <header className="pm-navbar">
      <div className="pm-nav-content">
        {/* Left Section */}
        <div className="pm-nav-left">
          <Link to="/sales-manager" className="pm-logo">
            <span className="pm-logo-text">Sales Manager Panel</span>
          </Link>
        </div>

        {/* Right Section */}
        <div className="pm-nav-right">
          <button
            className="pm-auth-button pm-auth-outline"
            onClick={() => navigate('/products')}
          >
            Main Shop
          </button>
          <button
            className="pm-auth-button pm-logout"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default NavbarPM;