import React, { useState, useEffect } from 'react';
import { useCart } from '../../context/CartContext';
import Navbar from '../../components/customer/layout/Navbar';
import './Checkout.css';
import { CartItem, CartContextType } from '../../context/CartContext';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext'; // Import AuthContext for user details

interface ShippingInfo {
  name: string;
  surname: string;
  email: string;
  address: string;
  taxID: string;
}

interface PaymentInfo {
  cardNumber: string;
  cardHolder: string;
  expiryDate: string;
  cvv: string;
}

const Checkout: React.FC = () => {
  const { cart, total, clearCart } = useCart() as CartContextType;
  const { user } = useAuth(); // Get logged-in user info
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<number>(2); // Start from payment step
  const [shippingInfo, setShippingInfo] = useState<ShippingInfo | null>(null);
  const [paymentInfo, setPaymentInfo] = useState<PaymentInfo>({
    cardNumber: '',
    cardHolder: '',
    expiryDate: '',
    cvv: ''
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [showConfirmationModal, setShowConfirmationModal] = useState(false);
  const [orderNumber, setOrderNumber] = useState<number | null>(null);
  const [invoiceHtml, setInvoiceHtml] = useState<string | null>(null);

  useEffect(() => {
    const fetchShippingInfo = async () => {
      try {
        if (!user) {
          throw new Error('User not logged in');
        }

        const response = await fetch(`http://localhost:8000/users/${user.userid}`);
        if (!response.ok) {
          throw new Error('Failed to fetch user information');
        }

        const data = await response.json();
        setShippingInfo({
          name: data.name,
          surname: data.surname,
          email: data.email,
          address: data.homeAddress,
          taxID: data.taxID
        });
      } catch (error) {
        console.error('Error fetching shipping info:', error);
      }
    };

    fetchShippingInfo();
  }, [user]);

  const handlePaymentInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    let formattedValue = value;

    if (name === 'cardNumber') {
      formattedValue = value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim();
      if (formattedValue.length > 19) return;
    }

    if (name === 'expiryDate') {
      formattedValue = value.replace(/\D/g, '').replace(/(\d{2})(\d{0,2})/, '$1/$2');
      if (formattedValue.length > 5) return;
    }

    if (name === 'cvv') {
      if (value.length > 3) return;
    }

    setPaymentInfo(prev => ({
      ...prev,
      [name]: formattedValue
    }));
  };

  const handlePaymentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
  
    try {
      if (!user || !shippingInfo) {
        throw new Error('User or shipping information is missing');
      }
  
      // Prepare order data
      const orderData = {
        userid: user.userid,
        totalamount: total,
        items: cart.map(item => ({
          productid: item.productid,
          quantity: item.quantity,
          price: item.price
        }))
      };
  
      // Send order creation request with invoice
      const orderResponse = await fetch('http://localhost:8000/create_order_with_invoice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
  
      if (!orderResponse.ok) {
        const errorData = await orderResponse.json();
        throw new Error(errorData.detail || 'Failed to create order');
      }
  
      const orderResult = await orderResponse.json();
      setOrderNumber(orderResult.orderid);
      setInvoiceHtml(orderResult.invoice_html); // Store the invoice HTML for rendering
  
      // Empty the cart
      const cartResponse = await fetch(`http://localhost:8000/cart/empty?userid=${user.userid}`, {
        method: 'DELETE'
      });
  
      if (!cartResponse.ok) {
        const errorData = await cartResponse.json();
        console.warn('Failed to empty cart:', errorData.detail);
      }
  
      clearCart();
      setCurrentStep(3);
      setShowConfirmationModal(true);
    } catch (error) {
      console.error('Error processing payment:', error);
    } finally {
      setIsProcessing(false);
    }
  };  

  const handleContinueShopping = () => {
    clearCart();
    navigate('/');
  };

  if (!shippingInfo) {
    return <div>Loading shipping information...</div>;
  }

  return (
    <div className="checkout-page">
      <Navbar onSearch={() => {}} />
      <div className="checkout-container">
        <div className="checkout-steps">
          <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>
            1. Payment
          </div>
          <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>
            2. Confirmation
          </div>
        </div>

        <div className="checkout-content">
          <div className="checkout-form">
            {currentStep === 2 && (
              <div className="payment-section">
                <h2>Shipping Information</h2>
                <div className="shipping-info">
                  <p>
                    <strong>Name:</strong> {shippingInfo.name} {shippingInfo.surname}
                  </p>
                  <p>
                    <strong>Email:</strong> {shippingInfo.email}
                  </p>
                  <p>
                    <strong>Address:</strong> {shippingInfo.address}
                  </p>
                  <p>
                    <strong>Tax ID:</strong> {shippingInfo.taxID}
                  </p>
                </div>

                <form onSubmit={handlePaymentSubmit}>
                  <h2>Payment Information</h2>
                  <div className="form-group">
                    <label htmlFor="cardNumber">Card Number</label>
                    <input
                      type="text"
                      id="cardNumber"
                      name="cardNumber"
                      value={paymentInfo.cardNumber}
                      onChange={handlePaymentInput}
                      placeholder="1234 5678 9012 3456"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="cardHolder">Card Holder Name</label>
                    <input
                      type="text"
                      id="cardHolder"
                      name="cardHolder"
                      value={paymentInfo.cardHolder}
                      onChange={handlePaymentInput}
                      placeholder="John Doe"
                      required
                    />
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label htmlFor="expiryDate">Expiry Date</label>
                      <input
                        type="text"
                        id="expiryDate"
                        name="expiryDate"
                        value={paymentInfo.expiryDate}
                        onChange={handlePaymentInput}
                        placeholder="MM/YY"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlFor="cvv">CVV</label>
                      <input
                        type="text"
                        id="cvv"
                        name="cvv"
                        value={paymentInfo.cvv}
                        onChange={handlePaymentInput}
                        placeholder="123"
                        required
                      />
                    </div>
                  </div>

                  <button type="submit" className="continue-btn" disabled={isProcessing}>
                    {isProcessing ? 'Processing...' : `Pay $${total.toFixed(2)}`}
                  </button>
                </form>
              </div>
            )}

            {currentStep === 3 && (
              <div className="confirmation-section">
                {isProcessing ? (
                  <div className="processing-payment">
                    <div className="loader"></div>
                    <h2>Processing Your Order</h2>
                    <p>Please don't close this page...</p>
                  </div>
                ) : (
                  <div className="success-message">
                    <div className="success-icon">✓</div>
                    <h2>Order Confirmed!</h2>
                    <p>Your order has been successfully placed.</p>
                    <p>Order #{orderNumber}</p>
                    {invoiceHtml && (
                      <div>
                        <h2>Invoice</h2>
                        <div
                          dangerouslySetInnerHTML={{ __html: invoiceHtml }}
                          className="invoice-html"
                        />
                      </div>
                    )}
                    <button className="continue-btn" onClick={handleContinueShopping}>
                      Continue Shopping
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="order-summary">
            <h2>Order Summary</h2>
            <div className="summary-items">
              {cart.map((item: CartItem) => (
                <div key={`${item.productid}}`} className="summary-item">
                  <img src={item.image} alt={item.productname} />
                  <div className="item-details">
                    <h3>{item.productname}</h3>
                    <p>Quantity: {item.quantity}</p>
                    <p>${item.price.toFixed(2)}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="summary-totals">
              <div className="subtotal">
                <span>Subtotal</span>
                <span>${total.toFixed(2)}</span>
              </div>
              <div className="shipping">
                <span>Shipping</span>
                <span>Free</span>
              </div>
              <div className="total">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;