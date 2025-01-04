import React, { useState, useEffect } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './Refund.css';
import { useParams } from 'react-router-dom';

interface Product {
  productid: number;
  name: string;
  image: string;
  quantity: number;
  price: number | null; // Allow null in case price is not available
}

interface RefundRequest {
  orderid: number;
  products: number[]; // List of product IDs
}

const Refund: React.FC = () => {
  const { orderId } = useParams<{ orderId: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  useEffect(() => {
    const fetchRefundableProducts = async () => {
      try {
        const response = await fetch(`http://localhost:8000/refund/select/${orderId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch refundable products');
        }
        const data = await response.json();

        const productDetails = await Promise.all(
          data.products.map(async (product: { productid: number; quantity: number }) => {
            const productResponse = await fetch(`http://localhost:8000/products/${product.productid}/`);
            if (!productResponse.ok) {
              throw new Error(`Failed to fetch details for product ID ${product.productid}`);
            }
            const productData = await productResponse.json();
            return {
              productid: product.productid,
              name: productData.productname,
              image: productData.image,
              quantity: product.quantity,
              price: productData.price ?? null, // Use null if price is unavailable
            };
          })
        );

        setProducts(productDetails);
      } catch (error) {
        console.error('Error fetching refundable products:', error);
      }
    };

    fetchRefundableProducts();
  }, [orderId]);

  const handleProductSelection = (productid: number) => {
    setSelectedProducts((prev) => {
      if (prev.includes(productid)) {
        return prev.filter((id) => id !== productid);
      } else {
        return [...prev, productid];
      }
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const refundRequest: RefundRequest = {
      orderid: parseInt(orderId || '0'),
      products: selectedProducts,
    };

    try {
      const response = await fetch('http://localhost:8000/refund/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(refundRequest),
      });

      if (!response.ok) {
        throw new Error('Failed to submit refund request');
      }

      setShowConfirmation(true);
    } catch (error) {
      console.error('Error submitting refund request:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="refund-page">
      <Navbar onSearch={() => {}} />
      <div className="refund-container">
        <h1>Request a Refund</h1>
        
        {!showConfirmation ? (
          <div className="refund-form-container">
            <form onSubmit={handleSubmit} className="refund-form">
            <div className="order-info" style={{ marginBottom: '30px' }}>
            <h1>Order Number: {orderId}</h1>
              </div>

              <div className="form-group">
                <h3 style={{ marginBottom: '10px' }}>Select Products to Refund</h3>
                <div className="refund-items">
                  {products.map((product) => (
                    <div 
                      key={product.productid} 
                      className={`refund-item ${selectedProducts.includes(product.productid) ? 'selected' : ''}`} 
                      onClick={() => handleProductSelection(product.productid)}
                    >
                      <img src={product.image} alt={product.name} className="refund-item-image" />
                      <div className="refund-item-details">
                        <h4>{product.name}</h4>
                        <p>Quantity: {product.quantity}</p>
                        <p>{product.price !== null ? `$${product.price.toFixed(2)}` : 'Price not available'}</p>
                      </div>
                      <div className="refund-select-indicator">
                        {selectedProducts.includes(product.productid) ? '●' : '○'}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <button 
                type="submit" 
                className={`submit-btn ${isSubmitting ? 'loading' : ''}`}
                disabled={isSubmitting || selectedProducts.length === 0}
              >
                {isSubmitting ? 'Submitting...' : 'Submit Refund Request'}
              </button>
            </form>

            <div className="refund-info">
              <h3>Refund Policy</h3>
              <ul>
                <li>Refund requests must be submitted within 30 days of purchase.</li>
                <li>Items must be unused and in original packaging.</li>
                <li>Shipping costs are non-refundable.</li>
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