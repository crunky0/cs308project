import React, { useState } from 'react';

function MyOrders() {
  // Mock order data
  const mockOrders = [
    {
      id: 1,
      date: '2024-11-20',
      status: 'Delivered',
      items: [
        { name: 'Smartphone', quantity: 1, price: 999.99 },
      ],
      total: 999.99,
    },
    {
      id: 2,
      date: '2024-11-22',
      status: 'In Transit',
      items: [
        { name: 'Laptop', quantity: 1, price: 1299.99 },
      ],
      total: 1299.99,
    },
  ];

  const [selectedOrder, setSelectedOrder] = useState(null);

  return (
    <div style={ordersPageStyle}>
      <h1>My Orders</h1>
      {mockOrders.map((order) => (
        <div key={order.id} style={orderCardStyle}>
          <h3>Order #{order.id}</h3>
          <p><strong>Date:</strong> {order.date}</p>
          <p><strong>Status:</strong> {order.status}</p>
          <p><strong>Total:</strong> ${order.total}</p>
          <button style={detailsButtonStyle} onClick={() => setSelectedOrder(order)}>
            View Details
          </button>
        </div>
      ))}

      {selectedOrder && (
        <div style={orderDetailsStyle}>
          <h3>Order Details</h3>
          <p><strong>Order ID:</strong> {selectedOrder.id}</p>
          <p><strong>Date:</strong> {selectedOrder.date}</p>
          <p><strong>Status:</strong> {selectedOrder.status}</p>
          <ul>
            {selectedOrder.items.map((item, index) => (
              <li key={index}>
                {item.quantity}x {item.name} - ${item.price}
              </li>
            ))}
          </ul>
          <p><strong>Total:</strong> ${selectedOrder.total}</p>
          <button style={closeButtonStyle} onClick={() => setSelectedOrder(null)}>
            Close
          </button>
        </div>
      )}
    </div>
  );
}

const ordersPageStyle = {
  textAlign: 'center',
  margin: '20px',
};

const orderCardStyle = {
  border: '1px solid #ddd',
  borderRadius: '5px',
  padding: '10px',
  margin: '10px auto',
  maxWidth: '500px',
};

const detailsButtonStyle = {
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px',
  cursor: 'pointer',
  borderRadius: '5px',
};

const orderDetailsStyle = {
  marginTop: '20px',
  padding: '20px',
  border: '1px solid #ddd',
  borderRadius: '5px',
};

const closeButtonStyle = {
  marginTop: '10px',
  backgroundColor: '#FF5733',
  color: 'white',
  border: 'none',
  padding: '10px',
  cursor: 'pointer',
  borderRadius: '5px',
};

export default MyOrders;
