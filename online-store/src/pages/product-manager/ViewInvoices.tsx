import React, { useEffect, useState } from "react";
import './ViewInvoices.css';

type Invoice = string;

const ViewInvoices: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [startDate, setStartDate] = useState<string>(""); // State for start date
  const [endDate, setEndDate] = useState<string>(""); // State for end date

  useEffect(() => {
    fetchInvoices();
  }, [startDate, endDate]); // Refetch invoices when dates change

  const fetchInvoices = async () => {
    try {
      const url = new URL("http://localhost:8000/productmanagerpanel/invoices");
      if (startDate) url.searchParams.append("start_date", startDate);
      if (endDate) url.searchParams.append("end_date", endDate);

      const response = await fetch(url.toString());
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

      {/* Date Filters */}
      <div className="filters">
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <button onClick={fetchInvoices} className="filter-btn">
          Filter
        </button>
      </div>

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