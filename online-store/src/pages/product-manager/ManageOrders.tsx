import React, { useEffect, useState } from "react";
import "./ManageOrders.css";

interface Order {
  orderid: number;
  userid: number;
  totalamount: number;
  orderdate: string;
  status: string;
  items: OrderItem[];
}

interface OrderItem {
  productid: number;
  quantity: number;
  productDetails?: ProductDetails;
}

interface ProductDetails {
  productname: string;
  image: string;
  price: number;
}

interface Delivery {
  deliveryid: number;
  orderid: number;
  customerid: number;
  productid: number;
  quantity: number;
  price: number; // From the deliveries table
  total_price: number; // From the deliveries table
  delivery_address: string;
  status: string;
  productDetails?: ProductDetails;
}

const ManageOrders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<string>("processing");

  useEffect(() => {
    if (filter === "processing") {
      fetchProcessingOrders();
    } else {
      fetchDeliveries(filter);
    }
  }, [filter]);

  const fetchProcessingOrders = async () => {
    try {
      const response = await fetch("http://localhost:8000/productmanagerpanel/orders/processing");
      if (!response.ok) throw new Error("Failed to fetch orders");
      const data = await response.json();

      const ordersWithDetails = await Promise.all(
        data.map(async (order: Order) => ({
          ...order,
          items: await Promise.all(
            order.items.map(async (item: OrderItem) => ({
              ...item,
              productDetails: await fetchProductDetails(item.productid),
            }))
          ),
        }))
      );

      setOrders(ordersWithDetails || []);
    } catch (err) {
      setError("Failed to load orders.");
    }
  };

  const fetchDeliveries = async (status: string) => {
    try {
      const response = await fetch("http://localhost:8000/productmanagerpanel/deliveries");
      if (!response.ok) throw new Error("Failed to fetch deliveries");
      const data = await response.json();

      const filteredDeliveries = data.deliveries.filter((delivery: Delivery) => delivery.status === status);

      const deliveriesWithDetails = await Promise.all(
        filteredDeliveries.map(async (delivery: Delivery) => ({
          ...delivery,
          productDetails: await fetchProductDetails(delivery.productid),
        }))
      );

      setDeliveries(deliveriesWithDetails || []);
    } catch (err) {
      setError("Failed to load deliveries.");
    }
  };

  const fetchProductDetails = async (productid: number): Promise<ProductDetails | null> => {
    try {
      const response = await fetch(`http://localhost:8000/products/${productid}/`);
      if (!response.ok) throw new Error("Failed to fetch product details");
      return await response.json();
    } catch (err) {
      console.error("Error fetching product details:", err);
      return null;
    }
  };

  const handleStartShipment = async (orderid: number) => {
    try {
      await fetch("http://localhost:8000/productmanagerpanel/deliveries/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ orderid }),
      });

      await fetch(`http://localhost:8000/productmanagerpanel/orders/${orderid}/status?status=in-transit`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
      });

      fetchProcessingOrders();
      fetchDeliveries(filter);
    } catch (err) {
      setError("Failed to start shipment.");
    }
  };

  const handleFinishDelivery = async (orderid: number) => {
    try {
      await fetch(`http://localhost:8000/productmanagerpanel/orders/${orderid}/status?status=delivered`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
      });

      fetchDeliveries(filter);
    } catch (err) {
      setError("Failed to finish delivery.");
    }
  };

  return (
    <div className="manage-orders-container">
      <h1>Manage Orders</h1>
      {error && <p className="error">{error}</p>}

      <div className="filter-buttons">
        {["processing", "in-transit", "delivered", "refunded"].map((status) => (
          <button
            key={status}
            className={`filter-btn ${filter === status ? "active" : ""}`}
            onClick={() => setFilter(status)}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      <div className="orders-list">
        {filter === "processing" ? (
          orders.length > 0 ? (
            orders.map((order) => (
              <div key={order.orderid} className="order-card">
                <h3>Order ID: {order.orderid}</h3>
                <p>Customer ID: {order.userid}</p>
                <p>Total Amount: ${order.totalamount.toFixed(2)}</p>
                <p>Order Date: {new Date(order.orderdate).toLocaleDateString()}</p>
                <div className="order-items">
                  {order.items.map((item, index) => (
                    <div key={index} className="order-item">
                      <img
                        src={item.productDetails?.image}
                        alt={item.productDetails?.productname}
                      />
                      <div>
                        <p>{item.productDetails?.productname}</p>
                        <p>Product ID: {item.productid}</p>
                        <p>Price: ${item.productDetails?.price.toFixed(2)}</p>
                        <p>Quantity: {item.quantity}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <button
                  onClick={() => handleStartShipment(order.orderid)}
                  className="start-shipment-btn"
                >
                  Start Shipment
                </button>
              </div>
            ))
          ) : (
            <p>No unshipped orders available.</p>
          )
        ) : (
          deliveries.length > 0 ? (
            deliveries.map((delivery) => (
              <div key={delivery.deliveryid} className="delivery-card">
                <h3>Delivery ID: {delivery.deliveryid}</h3>
                <p>Order ID: {delivery.orderid}</p>
                <p>Customer ID: {delivery.customerid}</p>
                <p>Delivery Address: {delivery.delivery_address}</p>
                <p className="delivery-status">Status: {delivery.status}</p>
                <div className="order-item">
                  <img
                    src={delivery.productDetails?.image}
                    alt={delivery.productDetails?.productname}
                  />
                  <div>
                    <p>{delivery.productDetails?.productname}</p>
                    <p>Product ID: {delivery.productid}</p>
                    <p>Price: ${delivery.price.toFixed(2)}</p>
                    <p>Total Order Price: ${delivery.total_price.toFixed(2)}</p>
                    <p>Quantity: {delivery.quantity}</p>
                  </div>
                </div>
                {delivery.status === "in-transit" && (
                  <button
                    onClick={() => handleFinishDelivery(delivery.orderid)}
                    className="finish-delivery-btn"
                  >
                    Finish Delivery
                  </button>
                )}
              </div>
            ))
          ) : (
            <p>No deliveries available for the selected status.</p>
          )
        )}
      </div>

    </div>
  );
};

export default ManageOrders;
