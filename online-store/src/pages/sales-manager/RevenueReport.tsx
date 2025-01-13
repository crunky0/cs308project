import React, { useState } from 'react';
import './RevenueReport.css';

const RevenuePage: React.FC = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [chartUrl, setChartUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchRevenueChartImage = async () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates.');
      return;
    }

    setLoading(true);
    setChartUrl(null); // Reset the chart URL before fetching

    try {
      const response = await fetch(
        `http://localhost:8000/profit_loss_chart_image?start_date=${startDate}&end_date=${endDate}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch the chart image.');
      }

      const imageBlob = await response.blob();
      const imageUrl = URL.createObjectURL(imageBlob);
      setChartUrl(imageUrl);
    } catch (error) {
      console.error(error);
      alert('Failed to fetch revenue chart image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="revenue-page-container">
      <h1>Revenue & Profit/Loss Report</h1>
      <div className="date-inputs">
        <label>Start Date:</label>
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        <label>End Date:</label>
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      </div>
      <button onClick={fetchRevenueChartImage} disabled={loading}>
        {loading ? 'Loading...' : 'Fetch Report'}
      </button>

      {chartUrl && (
        <div className="chart-container">
          <h2>Chart Image</h2>
          <img src={chartUrl} alt="Revenue & Profit/Loss Chart" />
        </div>
      )}
    </div>
  );
};

export default RevenuePage;
