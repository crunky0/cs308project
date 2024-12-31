import React, { useEffect, useState } from 'react';
import './ApproveComments.css';

interface Review {
  reviewid: number;
  userid: number;
  productid: number;
  rating: number;
  comment: string;
  approved: boolean;
  name?: string;
  surname?: string;
}

interface Product {
  productname: string;
  image: string;
}

const ApproveComments: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [productDetails, setProductDetails] = useState<{ [key: number]: Product }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch unapproved reviews
  const fetchReviews = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/reviews/not-approved/');
      if (!response.ok) {
        throw new Error('Failed to fetch reviews');
      }
      const data = await response.json();
      setReviews(data);

      // Fetch product details for each review
      for (const review of data) {
        await fetchProductDetails(review.productid);
      }
    } catch (err) {
      setError('Failed to fetch reviews. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch product details by ID
  const fetchProductDetails = async (productid: number) => {
    try {
      const response = await fetch(`http://localhost:8000/products/${productid}/`);
      if (!response.ok) {
        throw new Error(`Failed to fetch product with ID: ${productid}`);
      }
      const productData = await response.json();
      setProductDetails((prev) => ({ ...prev, [productid]: productData }));
    } catch (err) {
      setError('Failed to fetch product details. Please try again.');
    }
  };

  // Approve a review
  const handleApprove = async (reviewid: number) => {
    try {
      const response = await fetch(`http://localhost:8000/reviews/${reviewid}/approve/`, {
        method: 'PUT',
      });
      if (!response.ok) {
        throw new Error('Failed to approve the review');
      }
      setReviews(reviews.filter((review) => review.reviewid !== reviewid));
    } catch (err) {
      setError('Failed to approve the review. Please try again.');
    }
  };

  // Delete a review
  const handleDelete = async (reviewid: number) => {
    try {
      const response = await fetch(`http://localhost:8000/reviews/${reviewid}/`, {
        method: 'DELETE',
      });
      if (response.status === 204) {
        setReviews(reviews.filter((review) => review.reviewid !== reviewid));
      } else {
        throw new Error('Failed to delete the review');
      }
    } catch (err) {
      setError('Failed to delete the review. Please try again.');
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  return (
    <div className="approve-comments-container">
      <h1>Approve Comments</h1>
      {loading && <p className="loading">Loading reviews...</p>}
      {error && <p className="error">{error}</p>}
      <ul>
        {reviews.map((review) => {
          const product = productDetails[review.productid];
          return (
            <li key={review.reviewid}>
              <p><strong>User:</strong> {review.name} {review.surname}</p>
              {product ? (
                <>
                  <p><strong>Product:</strong> {product.productname}</p>
                  <img src={product.image} alt={product.productname} className="approve-comments-product-image" />
                </>
              ) : (
                <p>Loading product details...</p>
              )}
              <p><strong>Rating:</strong> {review.rating}</p>
              <p><strong>Comment:</strong> {review.comment}</p>
              <button onClick={() => handleApprove(review.reviewid)} className="approve-btn">
                <span className="material-icons">check_circle</span> Approve
              </button>
              <button onClick={() => handleDelete(review.reviewid)} className="delete-btn">
                <span className="material-icons">delete</span> Delete
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default ApproveComments;