import React, { useState, useEffect } from 'react';

const ViewInvoices = () => {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    // Fetch invoices from API
    const fetchInvoices = async () => {
      const response = await fetch('/api/invoices');
      const data = await response.json();
      setInvoices(data);
    };
    fetchInvoices();
  }, []);

  return (
    <div>
      <h2>Invoices</h2>
      <ul>
        {invoices.map(invoice => (
          <li key={invoice.id}>
            <span>Invoice #{invoice.id}</span>
            <p>Amount: {invoice.amount}</p>
            <p>Status: {invoice.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ViewInvoices;