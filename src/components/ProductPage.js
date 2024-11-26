import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';

function ProductPage() {
  const { productId } = useParams();

  // Mock product data
  const mockProducts = [
    {
      id: 1,
      name: "Smartphone",
      description: "Latest model smartphone with great features",
      price: 999.99,
      stock: 5, // In stock
      details: "This smartphone comes with a 6.5-inch display, 128GB storage, and a 5000mAh battery.",
      images: [
        "https://via.placeholder.com/300x300?text=Smartphone+Image+1",
        "https://via.placeholder.com/300x300?text=Smartphone+Image+2",
      ],
    },
    {
      id: 2,
      name: "Laptop",
      description: "High-performance laptop for work and play",
      price: 1299.99,
      stock: 0, // Out of stock
      details: "A laptop with 15.6-inch display, 512GB SSD, 16GB RAM, and 10-hour battery life.",
      images: [
        "https://via.placeholder.com/300x300?text=Laptop+Image+1",
        "https://via.placeholder.com/300x300?text=Laptop+Image+2",
      ],
    },
    {
      id: 3,
      name: "Headphones",
      description: "Noise-cancelling wireless headphones",
      price: 199.99,
      stock: 10, // In stock
      details: "Wireless headphones with active noise cancellation and 20-hour battery life.",
      images: [
        "https://via.placeholder.com/300x300?text=Headphones+Image+1",
        "https://via.placeholder.com/300x300?text=Headphones+Image+2",
      ],
    },
  ];

  // Find the selected product by ID
  const product = mockProducts.find((p) => p.id === parseInt(productId, 10));

  const [rating, setRating] = useState(0); // Current selected rating (0 to 5)
  const [hoverRating, setHoverRating] = useState(0); // Rating based on mouse hover
  const [comment, setComment] = useState(''); // Comment text
  const [showSubmit, setShowSubmit] = useState(false); // Control Submit button visibility

  const handleRatingClick = (newRating) => {
    setRating(newRating);
    setShowSubmit(true); // Show Submit button after clicking a rating
  };

  const handleCommentChange = (e) => {
    setComment(e.target.value);
  };

  const handleSubmit = () => {
    console.log('Comment:', comment);
    console.log('Rating:', rating);
    alert('Your rating and comment have been submitted!');
    setComment('');
    setRating(0);
    setShowSubmit(false); // Reset state
  };

  if (!product) {
    return (
      <div style={productPageStyle}>
        <h1>Product Not Found</h1>
        <Link to="/">Go Back to Home</Link>
      </div>
    );
  }

  return (
    <div style={productPageStyle}>
      <h1>{product.name}</h1>
      <div style={imageGalleryStyle}>
        {product.images.map((image, index) => (
          <img key={index} src={image} alt={`Product ${index + 1}`} style={imageStyle} />
        ))}
      </div>
      <p><strong>Description:</strong> {product.description}</p>
      <p><strong>Details:</strong> {product.details}</p>
      <p><strong>Price:</strong> ${product.price}</p>

      <div style={ratingBoxStyle}>
        <h3>Rate This Product</h3>
        <div style={starContainerStyle}>
          {[...Array(10)].map((_, index) => {
            const starValue = (index + 1) /2 ; // Allows half-star increments
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
    
        {showSubmit && (
        <button style={submitButtonStyle} onClick={handleSubmit}>
          Submit
        </button>
      )}
      <div style={commentBoxStyle}>
        <textarea
          placeholder="Add a comment..."
          value={comment}
          onChange={handleCommentChange}
          style={textAreaStyle}
        />
      </div>

      

      <Link to="/" style={backLinkStyle}>Go Back</Link>
    </div>
  );
}

const productPageStyle = {
  textAlign: 'center',
  margin: '20px',
  padding: '20px',
};

const imageGalleryStyle = {
  display: 'flex',
  justifyContent: 'center',
  gap: '10px',
  margin: '20px 0',
};

const imageStyle = {
  width: '300px',
  height: '300px',
  objectFit: 'cover',
  border: '1px solid #ddd',
  borderRadius: '5px',
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
