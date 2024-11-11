import React from 'react';
import ProductCard from './ProductCard';

function ProductList({ products, onAddToCart }) {
  return (
    <div style={listStyle}>
      {products.map((product) => (
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
