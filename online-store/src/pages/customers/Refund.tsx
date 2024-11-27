import React, { useState } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './Refund.css';
import { useParams } from 'react-router-dom';

interface RefundRequest {
  orderNumber: string;
  reason: string;
  description: string;
  email: string;
}

const Refund: React.FC = () => {
  const { orderId } = useParams();
  const [refundInfo, setRefundInfo] = useState<RefundRequest>({
    orderNumber: orderId || '',
    reason: '',
    description: '',
    email: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const reasons = [
    'Wrong size',
    'Damaged product',
    'Not as described',
    'Changed mind',
    'Other'
  ];

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setRefundInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setShowConfirmation(true);
    }, 1500);
  };

  return (
    <div className="refund-page">
      <Navbar onSearch={() => {}} />
      <div className="refund-container">
        <h1>Request a Refund</h1>
        
        {!showConfirmation ? (
          <div className="refund-form-container">
            <form onSubmit={handleSubmit} className="refund-form">
              <div className="form-group">
                <label htmlFor="orderNumber">Order Number*</label>
                <input
                  type="text"
                  id="orderNumber"
                  name="orderNumber"
                  value={refundInfo.orderNumber}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter your order number"
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email Address*</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={refundInfo.email}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter your email address"
                />
              </div>

              <div className="form-group">
                <label htmlFor="reason">Reason for Refund*</label>
                <select
                  id="reason"
                  name="reason"
                  value={refundInfo.reason}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a reason</option>
                  {reasons.map(reason => (
                    <option key={reason} value={reason}>
                      {reason}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="description">Description*</label>
                <textarea
                  id="description"
                  name="description"
                  value={refundInfo.description}
                  onChange={handleInputChange}
                  required
                  placeholder="Please provide more details about your refund request"
                  rows={4}
                />
              </div>

              <button 
                type="submit" 
                className={`submit-btn ${isSubmitting ? 'loading' : ''}`}
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Submitting...' : 'Submit Refund Request'}
              </button>
            </form>

            <div className="refund-info">
              <h3>Refund Policy</h3>
              <ul>
                <li>Refund requests must be submitted within 30 days of purchase</li>
                <li>Items must be unused and in original packaging</li>
                <li>Shipping costs are non-refundable</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="refund-confirmation">
            <h2>Refund Request Submitted</h2>
            <p>Thank you for submitting your refund request. Our team will review your request and process it accordingly.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Refund; 