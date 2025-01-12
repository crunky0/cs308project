import React, { useEffect, useState } from "react";
import './ViewInvoices.css';

type Invoice = string;

const ViewInvoices: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      const response = await fetch("http://localhost:8000/productmanagerpanel/invoices");
      if (!response.ok) throw new Error("Failed to fetch invoices");
      const data = await response.json();
      setInvoices(data || []);
    } catch (err) {
      setError("Failed to load invoices. Please try again later.");
    }
  };

  const handleViewInvoice = (filename: string) => {
    setSelectedInvoice(`http://localhost:8000/productmanagerpanel/invoices/${filename}`);
  };

  return (
    <div className="view-invoices-container">
  <h1>View Invoices</h1>
  {error && <p className="error">{error}</p>}

  <div className="content">
    {/* Left: Invoice List */}
    <div className="invoice-list">
      {invoices.length > 0 ? (
        invoices.map((filename) => (
          <div key={filename} className="invoice-item">
            <p>{filename}</p>
            <button
              onClick={() => handleViewInvoice(filename)}
              className="view-btn"
            >
              View
            </button>
          </div>
        ))
      ) : (
        <p>No invoices available.</p>
      )}
    </div>

    {/* Right: PDF Viewer */}
    <div className="pdf-viewer">
      {selectedInvoice ? (
        <iframe
          src={selectedInvoice}
          title="Invoice Viewer"
          width="100%"
          height="600px"
          style={{ border: "1px solid #ccc" }}
        />
      ) : (
        <p>Select an invoice to view</p>
      )}
    </div>
  </div>
</div>


  );
};

export default ViewInvoices;