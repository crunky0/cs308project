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
    <header className="am-navbar">
      <div className="am-nav-content">
        {/* Left Section */}
        <div className="am-nav-left">
          <Link to="/sales-manager" className="am-logo">
            <span className="am-logo-text">Sales Manager Panel</span>
          </Link>
        </div>

        {/* Right Section */}
        <div className="am-nav-right">
          <button
            className="am-auth-button am-auth-outline"
            onClick={() => navigate('/products')}
          >
            Main Shop
          </button>
          <button
            className="am-auth-button am-logout"
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