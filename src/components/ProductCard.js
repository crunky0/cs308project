import React from 'react';
import { Link } from 'react-router-dom';

function ProductCard({ product, onAddToCart }) {
  return (
    <div style={cardStyle}>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p><strong>Price:</strong> ${product.price}</p>
      <Link to={`/product/${product.id}`} style={detailsLinkStyle}>
        View Details
      </Link>
      <button style={buttonStyle} onClick={() => onAddToCart(product)}>
        Add to Cart
      </button>
    </div>
  );
}

const cardStyle = {
  border: '1px solid #ddd',
  borderRadius: '5px',
  padding: '10px',
  width: '200px',
  textAlign: 'center',
};

const buttonStyle = {
  backgroundColor: '#28a745',
  color: 'white',
  border: 'none',
  padding: '10px',
  cursor: 'pointer',
  borderRadius: '5px',
  marginTop: '10px',
};

const detailsLinkStyle = {
  display: 'block',
  marginTop: '10px',
  textDecoration: 'none',
  color: '#007BFF',
};

export default ProductCard;
