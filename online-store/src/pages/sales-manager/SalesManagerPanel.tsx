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
        <Link to="/sales-panel/manage-prices" className="sales-manager-link">Manage Prices</Link>
        <Link to="/sales-panel/view-invoices" className="sales-manager-link">View Invoices</Link>
        <Link to="/sales-panel/revenue-report" className="sales-manager-link"> Revenue Report</Link>
        </ul>
      </nav>
      <div className="sales-manager-content">
        <Outlet />
      </div>
    </div>
  );
};

export default SalesManagerPanel;
