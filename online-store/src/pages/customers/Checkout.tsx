import React, { useState } from 'react';
import { useCart } from '../../context/CartContext';
import Navbar from '../../components/customer/layout/Navbar';
import './Checkout.css';
import { CartItem, CartContextType } from '../../context/CartContext';
import { useNavigate } from 'react-router-dom';

interface ShippingInfo {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
}

interface PaymentInfo {
  cardNumber: string;
  cardHolder: string;
  expiryDate: string;
  cvv: string;
}

const Checkout: React.FC = () => {
  const { cart, total, clearCart } = useCart() as CartContextType;
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [shippingInfo, setShippingInfo] = useState<ShippingInfo>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: ''
  });
  const [paymentInfo, setPaymentInfo] = useState<PaymentInfo>({
    cardNumber: '',
    cardHolder: '',
    expiryDate: '',
    cvv: ''
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [showConfirmationModal, setShowConfirmationModal] = useState(false);
  const [orderNumber] = useState(Math.floor(100000 + Math.random() * 900000));

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setShippingInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentStep(2);
  };

  const handlePaymentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    setCurrentStep(3);
    
    setTimeout(() => {
      setIsProcessing(false);
      setShowConfirmationModal(true);
    }, 2000);
  };

  const handleContinueShopping = () => {
    clearCart();
    navigate('/');
  };

  return (
    <div className="checkout-page">
      <Navbar onSearch={() => {}} />
      <div className="checkout-container">
        <div className="checkout-steps">
          <div className={`step ${currentStep >= 1 ? 'active' : ''}`}>
            1. Shipping
          </div>
          <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>
            2. Payment
          </div>
          <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>
            3. Confirmation
          </div>
        </div>

        <div className="checkout-content">
          <div className="checkout-form">
            {currentStep === 1 && (
              <form onSubmit={handleSubmit}>
                <h2>Shipping Information</h2>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={shippingInfo.firstName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="lastName">Last Name</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={shippingInfo.lastName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={shippingInfo.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="phone">Phone</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={shippingInfo.phone}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="address">Address</label>
                  <input
                    type="text"
                    id="address"
                    name="address"
                    value={shippingInfo.address}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="city">City</label>
                    <input
                      type="text"
                      id="city"
                      name="city"
                      value={shippingInfo.city}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="state">State</label>
                    <input
                      type="text"
                      id="state"
                      name="state"
                      value={shippingInfo.state}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="zipCode">ZIP Code</label>
                    <input
                      type="text"
                      id="zipCode"
                      name="zipCode"
                      value={shippingInfo.zipCode}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <button type="submit" className="continue-btn">
                  Continue to Payment
                </button>
              </form>
            )}

            {currentStep === 2 && (
              <div className="payment-section">
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

                  <button type="submit" className="continue-btn">
                    Pay ${total.toFixed(2)}
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
                    <p>Order #{Math.floor(100000 + Math.random() * 900000)}</p>
                    <button 
                      className="continue-btn"
                      onClick={() => navigate('/')}
                    >
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
                <div key={`${item.productid}-${item.size}`} className="summary-item">
                  <img src={item.image} alt={item.productname} />
                  <div className="item-details">
                    <h3>{item.productname}</h3>
                    <p>Size: {item.size}</p>
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

      {showConfirmationModal && (
        <div className="modal-overlay">
          <div className="confirmation-modal">
            <div className="success-icon">✓</div>
            <h2>Payment Successful!</h2>
            <p>Thank you for your purchase</p>
            <p>Order #{orderNumber}</p>
            
            <div className="order-details">
              <p>Amount Paid: ${total.toFixed(2)}</p>
              <p>Shipping to: {shippingInfo.firstName} {shippingInfo.lastName}</p>
              <p>{shippingInfo.address}</p>
              <p>{shippingInfo.city}, {shippingInfo.state} {shippingInfo.zipCode}</p>
            </div>

            <div className="buttons">
              <button 
                className="continue-btn"
                onClick={handleContinueShopping}
              >
                Continue Shopping
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Checkout; 