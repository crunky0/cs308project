import React, { useState } from 'react';
import ProductCard from './ProductCard';

function ProductList({ searchQuery, sortOption, onSort, onAddToCart }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const mockProducts = [
    {
      id: 1,
      name: "Smartphone",
      description: "Latest model smartphone with great features",
      price: 999.99,
      stock: 5,
      rating: 4.5,
    },
    {
      id: 2,
      name: "Laptop",
      description: "High-performance laptop for work and play",
      price: 1299.99,
      stock: 0,
      rating: 4.8,
    },
    {
      id: 3,
      name: "Headphones",
      description: "Noise-cancelling wireless headphones",
      price: 199.99,
      stock: 10,
      rating: 4.2,
    },
  ];

  const filteredProducts = mockProducts
    .filter(
      (product) =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      if (sortOption === 'price-asc') return a.price - b.price;
      if (sortOption === 'price-desc') return b.price - a.price;
      if (sortOption === 'rating-asc') return a.rating - b.rating;
      if (sortOption === 'rating-desc') return b.rating - a.rating;
      return 0;
    });

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <div>
      <div style={sortButtonContainer}>
        <button style={sortButtonStyle} onClick={toggleDropdown}>
          Sort
        </button>
        {isDropdownOpen && (
          <div style={dropdownStyle}>
            <button onClick={() => onSort('price-asc')} style={dropdownItemStyle}>
              Price: Low to High
            </button>
            <button onClick={() => onSort('price-desc')} style={dropdownItemStyle}>
              Price: High to Low
            </button>
            <button onClick={() => onSort('rating-asc')} style={dropdownItemStyle}>
              Rating: Low to High
            </button>
            <button onClick={() => onSort('rating-desc')} style={dropdownItemStyle}>
              Rating: High to Low
            </button>
          </div>
        )}
      </div>

      <div style={listStyle}>
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} onAddToCart={onAddToCart} />
          ))
        ) : (
          <p>No products found for "{searchQuery}"</p>
        )}
      </div>
    </div>
  );
}

const sortButtonContainer = {
  position: 'relative',
  marginBottom: '20px',
};

const sortButtonStyle = {
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  borderRadius: '5px',
  cursor: 'pointer',
};

const dropdownStyle = {
  position: 'absolute',
  top: '40px',
  left: '0',
  backgroundColor: 'white',
  border: '1px solid #ddd',
  borderRadius: '5px',
  boxShadow: '0px 4px 6px rgba(0,0,0,0.1)',
  zIndex: 1,
};

const dropdownItemStyle = {
  display: 'block',
  padding: '10px',
  textAlign: 'left',
  backgroundColor: 'white',
  border: 'none',
  cursor: 'pointer',
  width: '100%',
};

const listStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '20px',
  justifyContent: 'center',
  padding: '20px',
};

export default ProductList;
