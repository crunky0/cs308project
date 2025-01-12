import React, { useState, useEffect } from 'react';
import './ManageProducts.css';

interface Product {
  productid: number;
  productname: string;
  categoryid: number;
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
    productname: '',
    productmodel: '',
    description: '',
    distributerinfo: '',
    warranty: '',
    stock: 0,
    categoryid: 0,
    image: '',
  });
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [newStock, setNewStock] = useState(0);
  const [categories, setCategories] = useState<{ categoryid: number; name: string }[]>([]);

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

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/productmanagerpanel/categories');
      if (!response.ok) {
        throw new Error('Failed to fetch categories');
      }
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      setError('Failed to load categories. Please try again.');
    }
  };
  
  // Fetch categories when the component mounts
  useEffect(() => {
    fetchCategories();
  }, []);

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
      const url = `http://localhost:8000/productmanagerpanel/products/${editingProduct.productid}/stock?stock=${newStock}`;
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Failed to update stock');
      }
      const data = await response.json();
      setProducts(
        products.map((product) =>
          product.productid === editingProduct.productid
            ? { ...product, stock: data.new_stock }
            : product
        )
      );
      setIsEditModalOpen(false);
    } catch (err) {
      setError('Failed to update stock. Please try again.');
    }
  };

  // Add a new product
  // Add a new product
  const handleAddProduct = async () => {
    try {
      const queryString = new URLSearchParams({
        productname: newProduct.productname,
        productmodel: newProduct.productmodel,
        description: newProduct.description,
        distributerinfo: newProduct.distributerinfo,
        warranty: newProduct.warranty,
        stock: newProduct.stock.toString(),
        categoryid: newProduct.categoryid.toString(),
        image: newProduct.image,
      }).toString();
  
      const response = await fetch(`http://localhost:8000/productmanagerpanel/products?${queryString}`, { // Use query parameters
        method: 'POST',
      });
  
      if (!response.ok) {
        throw new Error('Failed to add product');
      }
  
      const addedProduct = await response.json();
      setProducts([...products, addedProduct]); // Update the products list
      setNewProduct({
        productname: '',
        productmodel: '',
        description: '',
        distributerinfo: '',
        warranty: '',
        stock: 0,
        categoryid: 0,
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
  {products.map((product) => {
    const categoryName = categories.find((cat) => cat.categoryid === product.categoryid)?.name || 'Unknown';
    return (
      <div key={product.productid} className="product-card">
        <img src={product.image} alt={product.productname} className="product-image" />
        <h2>{product.productname}</h2>
        <p><strong>Category:</strong> {categoryName}</p>
        <p>
          <strong>Price:</strong> ${product.price !== undefined && product.price !== null ? product.price.toFixed(2) : 'N/A'}
        </p>
        {product.discountprice !== undefined && product.discountprice !== null && (
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
    );
  })}
</div>


      {/* Add Product Modal */}
      {isAddModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Product</h2>
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
              placeholder="Distributor Info"
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
              placeholder="Stock"
              value={newProduct.stock}
              onChange={(e) => setNewProduct({ ...newProduct, stock: parseInt(e.target.value, 10) })}
            />
            <select
              value={newProduct.categoryid}
              onChange={(e) => setNewProduct({ ...newProduct, categoryid: parseInt(e.target.value, 10) })}
            >
              <option value="" disabled>Select a Category</option>
              {categories.map((category) => (
                <option key={category.categoryid} value={category.categoryid}>
                  {category.name}
                </option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Image URL"
              value={newProduct.image}
              onChange={(e) => setNewProduct({ ...newProduct, image: e.target.value })}
            />
            <button onClick={handleAddProduct} className="add-btn">Add Product</button>
            <button onClick={() => setIsAddModalOpen(false)} className="cancel-btn">Cancel</button>
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
            <button onClick={handleEditStock} className="add-btn">Update Stock</button>
            <button onClick={() => setIsEditModalOpen(false)} className="cancel-btn">Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManageProducts;