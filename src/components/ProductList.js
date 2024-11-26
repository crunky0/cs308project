import React from 'react';
import ProductCard from './ProductCard';

function ProductList({ onAddToCart }) {
  const mockProducts = [
    {
      id: 1,
      name: "Smartphone",
      description: "Latest model smartphone with great features",
      price: 999.99,
      stock: 5,
    },
    {
      id: 2,
      name: "Laptop",
      description: "High-performance laptop for work and play",
      price: 1299.99,
      stock: 0,
    },
    {
      id: 3,
      name: "Headphones",
      description: "Noise-cancelling wireless headphones",
      price: 199.99,
      stock: 10,
    },
  ];

  return (
    <div style={listStyle}>
      {mockProducts.map((product) => (
        <ProductCard key={product.id} product={product} onAddToCart={onAddToCart} />
      ))}
    </div>
  );
}

const listStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '20px',
  justifyContent: 'center',
  padding: '20px',
};

export default ProductList;
