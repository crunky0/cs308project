import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './RevenueReport.css';

// Register chart components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface RevenueData {
  date: string;
  revenue: number;
  profit: number;
}

const RevenueReport: React.FC = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [revenueData, setRevenueData] = useState<RevenueData[]>([]);

  const fetchRevenue = async () => {
    try {
      const response = await fetch(`http://localhost:8000/revenue?start=${startDate}&end=${endDate}`);
      if (!response.ok) throw new Error('Failed to fetch revenue data');
      const data = await response.json();
      setRevenueData(data);
    } catch (err) {
      console.error(err);
    }
  };

  const chartData = {
    labels: revenueData.map((item) => item.date),
    datasets: [
      {
        label: 'Revenue',
        data: revenueData.map((item) => item.revenue),
        borderColor: 'green',
        backgroundColor: 'lightgreen',
      },
      {
        label: 'Profit/Loss',
        data: revenueData.map((item) => item.profit),
        borderColor: 'blue',
        backgroundColor: 'lightblue',
      },
    ],
  };

  return (
    <div className="revenue-report-container">
      <h1>Revenue Report</h1>
      <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      <button onClick={fetchRevenue}>Fetch Report</button>
      <Line data={chartData} />
    </div>
  );
};

export default RevenueReport;
