import React from 'react';
import { Link } from 'react-router-dom';

function ProductCard({ product, onAddToCart }) {
  return (
    <div style={cardStyle}>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p><strong>Price:</strong> ${product.price}</p>
      <p style={{ color: product.stock > 0 ? 'green' : 'red' }}>
        {product.stock > 0 ? `In Stock: ${product.stock}` : 'Out of Stock'}
      </p>
      <Link to={`/product/${product.id}`} style={detailsLinkStyle}>
        View Details
      </Link>
      <button
        style={{
          ...buttonStyle,
          backgroundColor: product.stock > 0 ? '#28a745' : '#ccc',
          cursor: product.stock > 0 ? 'pointer' : 'not-allowed',
        }}
        onClick={() => product.stock > 0 && onAddToCart(product)}
        disabled={product.stock === 0}
      >
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
  color: 'white',
  border: 'none',
  padding: '10px',
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
