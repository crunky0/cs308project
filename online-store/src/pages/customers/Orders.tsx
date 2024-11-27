import React from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './Orders.css';
import { useNavigate } from 'react-router-dom';

interface OrderItem {
  id: string;
  name: string;
  quantity: number;
  price: number;
  imageUrl: string;
}

interface Order {
  id: string;
  date: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  items: OrderItem[];
  total: number;
}

const OrdersPage: React.FC = () => {
  const navigate = useNavigate();

  // This would typically come from an API call
  const orders: Order[] = [
    {
      id: 'ORD-123',
      date: '2024-11-20',
      status: 'delivered',
      items: [
        {
          id: '1',
          name: 'Sample Product',
          quantity: 2,
          price: 29.99,
          imageUrl: '/sample-product.jpg'
        }
      ],
      total: 59.98
    }
  ];

  const getStatusColor = (status: Order['status']) => {
    const colors = {
      pending: 'var(--color-warning)',
      processing: 'var(--color-info)',
      shipped: 'var(--color-primary)',
      delivered: 'var(--color-success)',
      cancelled: 'var(--color-error)'
    };
    return colors[status];
  };

  const handleRefund = (orderId: string) => {
    navigate(`/refund/${orderId}`);
  };

  const isEligibleForRefund = (order: Order) => {
    const daysSinceOrder = (new Date().getTime() - new Date(order.date).getTime()) / (24 * 60 * 60 * 1000);
    return order.status === 'delivered' && daysSinceOrder <= 30;
  };

  return (
    <>
      <Navbar onSearch={() => {}} />
      <div className="orders-page">
        <h1>My Orders</h1>
        
        {orders.length === 0 ? (
          <div className="no-orders">
            <span className="material-icons">shopping_bag</span>
            <p>You haven't placed any orders yet</p>
          </div>
        ) : (
          <div className="orders-list">
            {orders.map((order) => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <div className="order-info">
                    <h3>Order #{order.id}</h3>
                    <p>Placed on {new Date(order.date).toLocaleDateString()}</p>
                  </div>
                  <div className="order-status" style={{ color: getStatusColor(order.status) }}>
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </div>
                </div>
                
                <div className="order-items">
                  {order.items.map((item) => (
                    <div key={item.id} className="order-item">
                      <img src={item.imageUrl} alt={item.name} className="item-image" />
                      <div className="item-details">
                        <h4>{item.name}</h4>
                        <p>Quantity: {item.quantity}</p>
                        <p>${item.price.toFixed(2)}</p>
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="order-footer">
                  <div className="order-total">
                    <span>Total:</span>
                    <span className="total-amount">${order.total.toFixed(2)}</span>
                  </div>
                  <div className="order-actions">
                    <button 
                      className="refund-btn"
                      onClick={() => handleRefund(order.id)}
                      disabled={!isEligibleForRefund(order)}
                      title={!isEligibleForRefund(order) ? "Refunds are only available for delivered orders within 30 days of purchase" : ""}
                    >
                      Request Refund
                    </button>
                    <button className="track-order-btn">Track Order</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default OrdersPage;