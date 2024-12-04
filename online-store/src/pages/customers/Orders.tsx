import React, { useState, useEffect } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './Orders.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext'; // Import AuthContext for user details

interface OrderItem {
  id: number;
  name: string;
  quantity: number;
  price: number;
  image: string; // Using 'image' as provided by the backend
}

interface Order {
  id: number;
  date: string;
  status: 'processing' | 'in-transit' | 'delivered';
  items: OrderItem[];
  total: number;
}

const OrdersPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth(); // Get logged-in user info
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        if (!user) {
          throw new Error('User not logged in');
        }

        const response = await fetch(`http://localhost:8000/orders/${user.userid}`);
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }

        const data = await response.json();
        const todayDate = new Date().toLocaleDateString();

        const formattedOrders = data.map((order: any) => ({
          id: order.orderid,
          date: todayDate, // Adjust if date format differs
          status: order.status,
          items: order.items.map((item: any) => ({
            id: item.productid,
            name: item.productname,
            quantity: item.quantity,
            price: item.price,
            image: item.image, // Backend provides 'image' field
          })),
          total: order.totalamount,
        }));
        setOrders(formattedOrders);
      } catch (error) {
        console.error('Error fetching orders:', error);
        setError('Failed to load orders. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [user]);

  const getStatusColor = (status: Order['status']) => {
    const colors = {
      processing: 'var(--color-info)',
      'in-transit': 'var(--color-primary)',
      delivered: 'var(--color-success)',
    };
    return colors[status];
  };

  const handleRefund = (orderId: number) => {
    navigate(`/refund/${orderId}`);
  };

  const isEligibleForRefund = (order: Order) => {
    const daysSinceOrder = (new Date().getTime() - new Date(order.date).getTime()) / (24 * 60 * 60 * 1000);
    return order.status === 'delivered' && daysSinceOrder <= 30;
  };

  if (loading) {
    return <div>Loading your orders...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

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
                      <img src={item.image} alt={item.name} className="item-image" />
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
