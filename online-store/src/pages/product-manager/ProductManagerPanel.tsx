import React from 'react';
import { Outlet , Link} from 'react-router-dom';
import NavbarPM from './NavbarPM'; // Import the new NavbarPM component
import './ProductManagerPanel.css'; // Import CSS for additional styles

const ProductManagerPanel = () => {
  return (
    <div className="pm-panel">
      <NavbarPM /> {/* Render the navbar at the top */}
      <nav className="pm-nav">
        <ul className="pm-menu">
          <li>
            <Link to="products" className="pm-link">
              Manage Products
            </Link>
          </li>
          <li>
            <Link to="categories" className="pm-link">
              Manage Categories
            </Link>
          </li>
          <li>
            <Link to="comments" className="pm-link">
              Approve Comments
            </Link>
          </li>
          <li>
            <Link to="orders" className="pm-link">
              Manage Orders
            </Link>
          </li>
          <li>
            <Link to="invoices" className="pm-link">
              View Invoices
            </Link>
          </li>
        </ul>
      </nav>
      <div className="pm-content">
        <Outlet />
      </div>
    </div>
  );
};

export default ProductManagerPanel;
