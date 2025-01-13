import React, { useState, useEffect } from 'react';
import './ManagePrices.css';

interface Product {
  productid: number;
  productname: string;
  price: number;
  discountprice?: number;
  image: string;
}

const ManagePrices: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);
  const [discount, setDiscount] = useState<number>(0);
  const [selectAll, setSelectAll] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState<boolean>(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [newPrice, setNewPrice] = useState<number | ''>('');

  useEffect(() => {
    fetchProducts();
  }, []);

  // Fetch products from the backend
  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:8000/products/');
      if (!response.ok) throw new Error('Failed to fetch products');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCheckboxChange = (productid: number) => {
    setSelectedProducts(prevSelected =>
      prevSelected.includes(productid)
        ? prevSelected.filter(id => id !== productid)
        : [...prevSelected, productid]
    );
  };

  // Handle product selection for price update
  const handleOpenPopup = (product: Product) => {
    setEditingProduct(product);
    setNewPrice(product.price);
    setIsPopupOpen(true);
  };

  // Handle price update
  const handleSetPrice = async () => {
    if (!editingProduct || newPrice === '') {
      alert('Please enter a valid price.');
      return;
    }
  
    try {
      const response = await fetch('http://localhost:8000/set_price', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          productid: editingProduct.productid,
          new_price: newPrice,
          discountprice: null, // Remove any existing discount
        }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to update product price');
      }
      setProducts(prevProducts =>
        prevProducts.map(product =>
          product.productid === editingProduct.productid
            ? { ...product, price: newPrice, discountprice: undefined }
            : product
        )
      );
  
      alert('Price updated successfully, and discount removed!');
      fetchProducts(); // Refresh product list
      setIsPopupOpen(false); // Close the popup
    } catch (error) {
      console.error(error);
      alert('Failed to update product price. Please try again.');
    }
  };
  

  // Apply bulk discount
  const applyBulkDiscount = async () => {
    if (selectedProducts.length === 0 || discount === 0) {
      alert('Please select at least one product and enter a discount rate.');
      return;
    }

    const updates = selectedProducts.map(productid => {
      const product = products.find(p => p.productid === productid);
      return product
        ? { productid: product.productid, discount_price: product.price - (product.price * discount) / 100 }
        : null;
    }).filter(update => update !== null);

    try {
      const response = await fetch(`http://localhost:8000/set_discounts_and_notify`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });

      if (!response.ok) throw new Error('Failed to apply discounts');

      alert('Discounts applied successfully and users notified!');
      fetchProducts();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="manage-prices-container">
      <h1>Manage Prices</h1>
      <div className="bulk-selection">
        <input type="checkbox" checked={selectAll} onChange={() => setSelectAll(!selectAll)} />
        <label>Select All Products</label>
      </div>
      <input
        type="number"
        placeholder="Enter discount %"
        value={discount}
        onChange={e => setDiscount(Number(e.target.value))}
      />
      <button onClick={applyBulkDiscount}>Apply Bulk Discount</button>
      <div className="sales-list">
        {products.map(product => (
          <div className="sales-card" onClick={() => handleOpenPopup(product)}>
            <input
              type="checkbox"
              checked={selectedProducts.includes(product.productid)}
              onChange={() => handleCheckboxChange(product.productid)}
            />
          <img src={product.image} alt={product.productname} />
          <h2>{product.productname}</h2>
          <p>Price: ${product.price.toFixed(2)}</p>
            {product.discountprice && <p>Discounted Price: ${product.discountprice.toFixed(2)}</p>}
            <button onClick={() => handleOpenPopup(product)}>Set Price</button>
          </div>

        ))}
      </div>

      {isPopupOpen && editingProduct && (
        <div className="popup">
          <div className="popup-content">
            <img src={editingProduct.image} alt={editingProduct.productname} />
            <h2>{editingProduct.productname}</h2>
            <p>Current Price: ${editingProduct.price.toFixed(2)}</p>
            <input
              type="number"
              placeholder="Enter new price"
              value={newPrice}
              onChange={e => setNewPrice(Number(e.target.value))}
            />
            <button onClick={handleSetPrice}>Update Price</button>
            <button onClick={() => setIsPopupOpen(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManagePrices;
