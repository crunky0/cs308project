import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import NavbarSM from './NavbarSM';
import './SalesManagerPanel.css';

const SalesManagerPanel = () => {
  return (
    <div className="sales-manager-panel">
      <NavbarSM />
      <h1 className="sales-manager-header">Sales Manager Panel</h1>
      <nav className="sales-manager-nav">
        <ul className="sales-manager-menu">
          <li>
            <Link to="manage-prices" className="sales-manager-link">Manage Prices</Link>
          </li>
          <li>
            <Link to="manage-prices" className="sales-manager-link">Manage Discount</Link>
          </li>
          <li>
            <Link to="sales-reports" className="sales-manager-link">View Sales Reports</Link>
          </li>
        </ul>
      </nav>
      <div className="sales-manager-content">
        <Outlet />
      </div>
    </div>
  );
};

export default SalesManagerPanel;
