import React from 'react';
import { Link } from 'react-router-dom';

interface NavbarProps {
  isSidebarOpen: boolean;
  setIsSidebarOpen: (isOpen: boolean) => void;
}

const Navbar: React.FC<NavbarProps> = ({ isSidebarOpen, setIsSidebarOpen }) => {
  return (
    <nav className={`navbar-fixed ${isSidebarOpen ? 'sidebar-open' : ''}`}>
      <div className="nav-content">
        <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="hamburger-button">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <span className="nav-title">Product Manager Dashboard</span>

        <button className="logout-button">Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;