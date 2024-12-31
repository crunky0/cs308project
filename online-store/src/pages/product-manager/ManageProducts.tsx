import React, { useState, useEffect } from 'react';
import './ManageProducts.css';

interface Product {
  productid: number;
  productname: string;
  categoryid: string;
  stock: number;
  price: number;
  discountprice?: number;
  image: string;
}

const ManageProducts: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [newProduct, setNewProduct] = useState({
    serialnumber: 0,
    productname: '',
    productmodel: '',
    description: '',
    distributerinfo: '',
    warranty: '',
    price: 0,
    cost: 0,
    stock: 0,
    categoryid: 0,
    soldamount: 0,
    discountprice: 0,
    image: '',
  });  
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [newStock, setNewStock] = useState(0);

  const getUserIdFromSession = () => {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    return user.userid || null;
  };
  

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

  // Delete a product
  const handleDeleteProduct = async (productid: number) => {
    try {
      const response = await fetch(`http://localhost:8000/products/${productid}/`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete product');
      }
      setProducts(products.filter((product) => product.productid !== productid));
    } catch (err) {
      setError('Failed to delete product. Please try again.');
    }
  };

  // Edit stock
  const handleEditStock = async () => {
    if (!editingProduct) return;
  
    try {
      const userId = getUserIdFromSession(); // Retrieve the logged-in user's ID
  
      const url = `http://localhost:8000/productmanagerpanel/products/${editingProduct.productid}/stock?stock=${newStock}`;
  
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        const errorResponse = await response.json();
        console.error('Error:', errorResponse);
        throw new Error(errorResponse.detail || 'Failed to update stock');
      }
  
      const data = await response.json();
      setProducts(
        products.map((product) =>
          product.productid === editingProduct.productid
            ? { ...product, stock: data.new_stock }
            : product
        )
      );
      setIsEditModalOpen(false); // Close modal after success
    } catch (err) {
      setError('Failed to update stock. Please try again.');
      console.error('Stock Update Error:', err);
    }
  };
  

  // Add a new product
  const handleAddProduct = async () => {
    try {
      const response = await fetch('http://localhost:8000/products/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProduct), // Send the product object as JSON
      });
  
      if (!response.ok) {
        throw new Error('Failed to add product');
      }
  
      const addedProduct = await response.json(); // Get the newly added product from the response
      setProducts([...products, addedProduct]); // Update the products list
      setNewProduct({
        serialnumber: 0,
        productname: '',
        productmodel: '',
        description: '',
        distributerinfo: '',
        warranty: '',
        price: 0,
        cost: 0,
        stock: 0,
        categoryid: 0,
        soldamount: 0,
        discountprice: 0,
        image: '',
      });
      setIsAddModalOpen(false); // Close the modal
    } catch (err) {
      setError('Failed to add product. Please try again.');
    }
  };  

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="manage-products-container">
      <h1>Manage Products</h1>
      {loading && <p>Loading products...</p>}
      {error && <p className="error">{error}</p>}
      <button className="add-btn" onClick={() => setIsAddModalOpen(true)}>Add Product</button>
      <div className="products-list">
        {products.map((product) => (
          <div key={product.productid} className="product-card">
            <img src={product.image} alt={product.productname} className="product-image" />
            <h2>{product.productname}</h2>
            <p><strong>Categoryid:</strong> {product.categoryid}</p>
            <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
            {product.discountprice && (
              <p><strong>Discount Price:</strong> ${product.discountprice.toFixed(2)}</p>
            )}
            <p><strong>Stock:</strong> {product.stock}</p>
            <button onClick={() => handleDeleteProduct(product.productid)} className="delete-btn">
              Delete
            </button>
            <button
              onClick={() => {
                setEditingProduct(product);
                setNewStock(product.stock);
                setIsEditModalOpen(true);
              }}
              className="edit-btn"
            >
              Edit Stock
            </button>
          </div>
        ))}
      </div>

      {/* Add Product Modal */}
      {isAddModalOpen && (
        <div className="modal-overlay">
            <div className="modal">
            <h2>Add New Product</h2>
            <input
                type="number"
                placeholder="Serial Number"
                value={newProduct.serialnumber}
                onChange={(e) => setNewProduct({ ...newProduct, serialnumber: parseInt(e.target.value, 10) })}
            />
            <input
                type="text"
                placeholder="Product Name"
                value={newProduct.productname}
                onChange={(e) => setNewProduct({ ...newProduct, productname: e.target.value })}
            />
            <input
                type="text"
                placeholder="Product Model"
                value={newProduct.productmodel}
                onChange={(e) => setNewProduct({ ...newProduct, productmodel: e.target.value })}
            />
            <textarea
                placeholder="Description"
                value={newProduct.description}
                onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
            />
            <input
                type="text"
                placeholder="Distributer Info"
                value={newProduct.distributerinfo}
                onChange={(e) => setNewProduct({ ...newProduct, distributerinfo: e.target.value })}
            />
            <input
                type="text"
                placeholder="Warranty"
                value={newProduct.warranty}
                onChange={(e) => setNewProduct({ ...newProduct, warranty: e.target.value })}
            />
            <input
                type="number"
                placeholder="Price"
                value={newProduct.price}
                onChange={(e) => setNewProduct({ ...newProduct, price: parseFloat(e.target.value) })}
            />
            <input
                type="number"
                placeholder="Cost"
                value={newProduct.cost}
                onChange={(e) => setNewProduct({ ...newProduct, cost: parseFloat(e.target.value) })}
            />
            <input
                type="number"
                placeholder="Stock"
                value={newProduct.stock}
                onChange={(e) => setNewProduct({ ...newProduct, stock: parseInt(e.target.value, 10) })}
            />
            <input
                type="number"
                placeholder="Category ID"
                value={newProduct.categoryid}
                onChange={(e) => setNewProduct({ ...newProduct, categoryid: parseInt(e.target.value, 10) })}
            />
            <input
                type="number"
                placeholder="Sold Amount"
                value={newProduct.soldamount}
                onChange={(e) => setNewProduct({ ...newProduct, soldamount: parseInt(e.target.value, 10) })}
            />
            <input
                type="number"
                placeholder="Discount Price (Optional)"
                value={newProduct.discountprice}
                onChange={(e) =>
                setNewProduct({ ...newProduct, discountprice: parseFloat(e.target.value) })
                }
            />
            <input
                type="text"
                placeholder="Image URL"
                value={newProduct.image}
                onChange={(e) => setNewProduct({ ...newProduct, image: e.target.value })}
            />
            <button onClick={handleAddProduct} className="add-btn">
                Add Product
            </button>
            <button onClick={() => setIsAddModalOpen(false)} className="cancel-btn">
                Cancel
            </button>
            </div>
        </div>
        )}


      {/* Edit Stock Modal */}
      {isEditModalOpen && editingProduct && (
        <div className="modal-overlay">
            <div className="modal">
            <h2>Edit Stock for {editingProduct.productname}</h2>
            <input
                type="number"
                value={newStock}
                onChange={(e) => setNewStock(parseInt(e.target.value, 10))}
                placeholder="Enter new stock amount"
            />
            <button onClick={handleEditStock} className="add-btn">
                Update Stock
            </button>
            <button onClick={() => setIsEditModalOpen(false)} className="cancel-btn">
                Cancel
            </button>
            </div>
        </div>
        )}
    </div>
  );
};

export default ManageProducts;
