import React, { useState, useEffect } from 'react';
import './ManageSales.css';
import { useNavigate } from 'react-router-dom';


interface Product {
  productid: number;
  productname: string;
  price: number;
  discountprice?: number;
  image: string;
}

const SalesManager: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [discountRate, setDiscountRate] = useState<number | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<number | null>(null);

  // Fetch all products
  const fetchProducts = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/products/');
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      setError('Failed to load products. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Apply discount to the selected product
  const applyDiscount = async () => {
    if (selectedProduct === null || discountRate === null) {
      alert('Please select a product and enter a discount rate.');
      return;
    }

    try {
      const product = products.find(p => p.productid === selectedProduct);
      if (!product) return;

      const newPrice = product.price * (1 - discountRate / 100);
      const response = await fetch(`http://localhost:8000/products/${selectedProduct}/discount`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ discountprice: newPrice }),
      });

      if (!response.ok) {
        throw new Error('Failed to apply discount');
      }

      setProducts(
        products.map(p =>
          p.productid === selectedProduct ? { ...p, discountprice: newPrice } : p
        )
      );
      alert('Discount applied successfully!');
    } catch (err) {
      setError('Failed to apply discount. Please try again.');
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="manage-products-container">
      <h1>Sales Manager</h1>
      {loading && <p>Loading products...</p>}
      {error && <p className="error">{error}</p>}

      <div className="products-list">
        {products.map(product => (
          <div key={product.productid} className="product-card">
            <img src={product.image} alt={product.productname} className="product-image" />
            <h2>{product.productname}</h2>
            <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
            {product.discountprice && (
              <p><strong>Discount Price:</strong> ${product.discountprice.toFixed(2)}</p>
            )}
            <button onClick={() => navigate('/sales-panel/manage-prices')} className="discount-btn">
            Select for Discount
            </button>

          </div>
        ))}
      </div>

      <div className="modal">
        <h2>Apply Discount</h2>
        <input
          type="number"
          placeholder="Enter discount rate (%)"
          value={discountRate ?? ''}
          onChange={e => setDiscountRate(parseFloat(e.target.value))}
        />
        <button onClick={applyDiscount} className="add-btn">
          Apply Discount
        </button>
      </div>
    </div>
  );
};

export default SalesManager;
