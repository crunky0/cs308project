import React, { useState, useEffect } from 'react';

const ManageOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    // Fetch orders from API
    const fetchOrders = async () => {
      const response = await fetch('/api/orders');
      const data = await response.json();
      setOrders(data);
    };
    fetchOrders();
  }, []);

  const handleChangeStatus = async (orderId: number, status: string) => {
    // API call to change status
    // Update state with new status
  };

  return (
    <div>
      <h2>Manage Orders</h2>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            <span>Order #{order.id}</span>
            <select
              value={order.status}
              onChange={(e) => handleChangeStatus(order.id, e.target.value)}
            >
              <option value="Pending">Pending</option>
              <option value="Shipped">Shipped</option>
              <option value="Delivered">Delivered</option>
            </select>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageOrders;