import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function ProductPage() {
  const { productId } = useParams();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [comment, setComment] = useState('');
  const [showSubmit, setShowSubmit] = useState(false);

  // Fetch product details from the backend
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/products/${productId}`);
        setProduct(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching product details. Please try again later.');
        setLoading(false);
      }
    };
    fetchProduct();
  }, [productId]);

  const handleRatingClick = (newRating) => {
    setRating(newRating);
    setShowSubmit(true);
  };

  const handleCommentChange = (e) => {
    setComment(e.target.value);
    setShowSubmit(e.target.value !== '' || rating > 0);
  };

  const handleSubmit = async () => {
    try {
      // Simulate sending the rating and comment to the backend
      const payload = { productId, rating, comment };
      await axios.post(`http://localhost:8000/products/${productId}/rate`, payload);
      alert('Your rating and comment have been submitted!');
      setComment('');
      setRating(0);
      setShowSubmit(false);
    } catch (err) {
      alert('Error submitting rating and comment. Please try again.');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div style={productPageStyle}>
      <h1>{product.productName}</h1>
      <p><strong>Model:</strong> {product.productModel}</p>
      <p><strong>Description:</strong> {product.description}</p>
      <p><strong>Distributer Info:</strong> {product.distributerInfo}</p>
      <p><strong>Warranty:</strong> {product.warranty}</p>
      <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
      <p><strong>Stock:</strong> {product.stock} items available</p>

      <div style={ratingBoxStyle}>
        <h3>Rate This Product</h3>
        <div style={starContainerStyle}>
          {[...Array(10)].map((_, index) => {
            const starValue = (index + 1) / 2;
            return (
              <span
                key={index}
                style={{
                  ...starStyle,
                  color: hoverRating >= starValue || rating >= starValue ? 'yellow' : 'gray',
                }}
                onMouseEnter={() => setHoverRating(starValue)}
                onMouseLeave={() => setHoverRating(0)}
                onClick={() => handleRatingClick(starValue)}
              >
                ★
              </span>
            );
          })}
        </div>
        <p>{rating > 0 ? `Rating: ${rating}/5` : 'No rating yet'}</p>
      </div>

      <div style={commentBoxStyle}>
        <textarea
          placeholder="Add a comment..."
          value={comment}
          onChange={handleCommentChange}
          style={textAreaStyle}
        />
      </div>

      {showSubmit && (
        <button style={submitButtonStyle} onClick={handleSubmit}>
          Submit
        </button>
      )}

      <Link to="/" style={backLinkStyle}>Go Back</Link>
    </div>
  );
}

const productPageStyle = {
  textAlign: 'center',
  margin: '20px',
  padding: '20px',
};



const ratingBoxStyle = {
  marginTop: '20px',
};

const starContainerStyle = {
  display: 'inline-block',
};

const starStyle = {
  fontSize: '30px',
  margin: '5px',
  cursor: 'pointer',
  transition: 'color 0.2s',
};

const commentBoxStyle = {
  marginTop: '20px',
};

const textAreaStyle = {
  width: '80%',
  height: '100px',
  padding: '10px',
  fontSize: '16px',
};

const submitButtonStyle = {
  marginTop: '20px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  cursor: 'pointer',
  borderRadius: '5px',
};

const backLinkStyle = {
  display: 'inline-block',
  marginTop: '20px',
  textDecoration: 'none',
  color: '#007BFF',
};

export default ProductPage;
