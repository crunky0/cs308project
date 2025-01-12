import React, { useState, useEffect } from 'react';
import './ManagePrices.css';

interface Product {
  productid: number;
  productname: string;
  price: number;
  discountprice?: number;
}

const ManagePrices: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [discount, setDiscount] = useState<number>(0);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:8000/products/');
      if (!response.ok) throw new Error('Failed to fetch products');
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      console.error(err);
    }
  };

  const applyDiscount = (product: Product, discount: number) => {
    const newPrice = product.price - (product.price * discount) / 100;
    setSelectedProduct({ ...product, discountprice: newPrice });
  };

  const notifyUsers = async (productid: number) => {
    try {
      const response = await fetch(`http://localhost:8000/notify-users/${productid}`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to notify users');
    } catch (err) {
      console.error(err);
    }
  };
  
  const handleSave = async (product: Product) => {
    try {
      const response = await fetch(`http://localhost:8000/products/${product.productid}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ discountprice: product.discountprice }),
      });
      if (!response.ok) throw new Error('Failed to update product price');
      fetchProducts();
      await notifyUsers(product.productid); // Notify users after updating the price
    } catch (err) {
      console.error(err);
    }
  };
  

  return (
    <div className="manage-prices-container">
      <h1 className="manage-prices-header">Manage Prices</h1>
      <div className="manage-prices-list">
        {products.map((product) => (
          <div key={product.productid} className="manage-prices-card">
            <h2>{product.productname}</h2>
            <p>Original Price: ${product.price.toFixed(2)}</p>
            <p>
              Discounted Price:{' '}
              {product.discountprice ? `$${product.discountprice.toFixed(2)}` : 'Not Set'}
            </p>
            <input
              type="number"
              placeholder="Enter discount %"
              value={discount}
              onChange={(e) => setDiscount(parseFloat(e.target.value))}
              className="manage-prices-input"
            />
            <button onClick={() => applyDiscount(product, discount)} className="manage-prices-btn">
              Apply Discount
            </button>
            <button onClick={() => handleSave(selectedProduct!)} className="manage-prices-save-btn">
              Save
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ManagePrices;
