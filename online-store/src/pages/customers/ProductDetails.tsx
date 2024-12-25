import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './ProductDetails.css';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext'; // Import AuthContext
import ReviewForm from '../../components/products/ReviewForm';

interface Review {
  reviewid: number;
  productid: number;
  userid: number;
  name: string;
  surname: string;
  rating: number;
  comment: string;
  date: string;
}

interface ProductDetails {
  productid: number;
  productname: string;
  price: number;
  image: string;
  description: string;
  rating?: number;
  reviews?: number;
  warranty: string;
  productmodel: string;
  stock: number;
}

const ProductDetails = () => {
  const { id } = useParams(); // productid from the URL
  const { addToCart } = useCart();
  const { user } = useAuth(); // Access logged-in user details
  const [product, setProduct] = useState<ProductDetails | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        setLoading(true);
    
        // Fetch product details
        const productResponse = await fetch(`http://localhost:8000/products/${id}/`);
        if (!productResponse.ok) {
          throw new Error('Failed to fetch product details');
        }
        const productData = await productResponse.json();
    
        // Fetch average rating
        const ratingResponse = await fetch(`http://localhost:8000/products/${id}/average-rating/`);
        const averageRating = ratingResponse.ok ? await ratingResponse.json() : null;
    
        // Fetch reviews
        const reviewsResponse = await fetch(`http://localhost:8000/products/${id}/reviews/`);
        const reviewsData = reviewsResponse.ok ? await reviewsResponse.json() : [];
    
        setProduct({ ...productData, rating: averageRating });
        setReviews(reviewsData);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('An unexpected error occurred');
        }
      } finally {
        setLoading(false);
      }
    };
    

    fetchProductDetails();
  }, [id]);

  const handleAddToCart = () => {
    if (!product || product.stock <= 0) {
      alert('Product is out of stock');
      return;
    }

    addToCart(product.productid, 1, user?.userid);



    setProduct((prev) =>
      prev ? { ...prev, stock: prev.stock - 1 } : null
    );
  };

  const handleSearch = (query: string) => {
    console.log('Search query:', query);
  };

  const handleReviewSubmit = async ({ rating, comment }: { rating: number; comment: string }) => {
    if (!user) {
      alert("You must be logged in to submit a review.");
      return;
    }
  
    try {
      const payload = {
        userid: user.userid,
        productid: product?.productid,
        rating,
        comment,
      };
  
      const response = await fetch(`http://localhost:8000/reviews/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit review');
      }
  
      // Yorum gönderimi başarılıysa, yeni yorumları fetch et
      const reviewsResponse = await fetch(`http://localhost:8000/products/${product?.productid}/reviews/`);
      const updatedReviews = reviewsResponse.ok ? await reviewsResponse.json() : [];
      setReviews(updatedReviews); // Yorumları güncelle
  
      alert("Your review has been submitted and is awaiting approval.");
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  };
  
  
  
  
  

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div className="product-details-page">
      <Navbar onSearch={handleSearch} />
      <div className="product-container">
        <div className="product-images">
          <img src={product.image} alt={product.productname} />
        </div>
        <div className="product-info">
          <h1>{product.productname}</h1>
          <p>{product.description}</p>
          {product.rating && (
            <div className="rating">
            <div className="stars">
              {Array.from({ length: 5 }).map((_, index) => {
                const fullValue = index + 1;
                const isFull = (product.rating ?? 0) >= fullValue;
                const isHalf = (product.rating ?? 0) > index && (product.rating ?? 0) < fullValue;
          
                return (
                  <span
                    key={index}
                    className={`star ${isFull ? 'full' : isHalf ? 'half' : ''}`}
                  >
                    ★
                  </span>
                );
              })}
            </div>
            <span className="rating-text">{product.rating.toFixed(1)} ({reviews.length} reviews)</span> {/* Dynamic review count */}
          </div>
          )}
          <div className="price">Price: ${product.price.toFixed(2)}</div>
          <div>Model: {product.productmodel}</div>
          <div>Warranty: {product.warranty}</div>
          <div>Stock: {product.stock}</div>
          <button className="add-to-cart-btn" onClick={handleAddToCart} disabled={product.stock <= 0}>
            Add to Cart
          </button>
        </div>
      </div>
      <div className="reviews-section">
  <h2>Reviews</h2>
  <ReviewForm onSubmit={handleReviewSubmit} />
  {reviews.map((review) => (
  <div key={review.reviewid} className="review-item">
    {/* Header Section */}
    <div className="review-header">
      <span className="reviewer-name">
        <strong>
          {review.name ? review.name : "Anonymous"} {review.surname ? review.surname : ""}
        </strong>
      </span>
      <span className="review-date">
        {review.date ? new Date(review.date).toLocaleDateString() : "Unknown Date"}
      </span>
    </div>

    {/* Rating Section */}
    <div className="review-rating">
      <span className="stars">
        {Array.from({ length: 5 }).map((_, index) => {
          if (review.rating > index) {
            if (review.rating - index >= 1) {
              return <span key={index} className="star full">★</span>; // Full star
            } else {
              return <span key={index} className="star partial">
                <span className="partial-fill" style={{ width: `${(review.rating - index) * 100}%` }}>★</span>
                <span className="empty-fill">★</span>
              </span>;
            }
          } else {
            return <span key={index} className="star empty">★</span>; // Empty star
          }
        })}
      </span>
      <span className="rating-number">{review.rating}/5</span>
    </div>

    {/* Comment Section */}
    <div className="review-body">
      {review.comment ? review.comment : "No comment provided."}
    </div>
  </div>

))}

</div>


    </div>
  );
};

export default ProductDetails;