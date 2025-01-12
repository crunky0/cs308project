import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import NavbarSM from './NavbarSM'; // Sales Manager specific Navbar
import './SalesManagerPanel.css';

const SalesManagerPanel = () => {
  return (
    <div className="sm-panel">
      <NavbarSM />
      <nav className="sm-nav">
        <ul className="sm-menu">
          <li>
            <Link to="sales" className="sm-link">
              Manage Discounts
            </Link>
          </li>
          <li>
            <Link to="notifications" className="sm-link">
              Notify Users
            </Link>
          </li>
          <li>
          <li>
            <Link to="manage-prices" className="sales-link">Manage Prices</Link>
          </li>
          <li>
            <Link to="sales-reports" className="sales-link">View Sales Reports</Link>
          </li>
            <Link to="reports" className="sm-link">
              Sales Reports
            </Link>
          </li>
        </ul>
      </nav>
      <div className="sm-content">
        <Outlet />
      </div>
    </div>
  );
};

export default SalesManagerPanel;
