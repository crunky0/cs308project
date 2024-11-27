import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import './ProductDetails.css';
import { useCart } from '../../context/CartContext';
import ReviewForm from '../../components/products/ReviewForm';

interface Review {
  id: number;
  user: string;
  rating: number;
  comment: string;
  date: string;
}

interface RatingDistribution {
  [key: number]: number;  // This allows numerical indexing
}

interface RatingStats {
  distribution: RatingDistribution;
  total: number;
}

interface ProductDetails {
  id: number;
  name: string;
  price: number;
  image: string;
  description: string;
  rating: number;
  reviews: number;
  sizes: string[];
  features: string[];
  specifications: Record<string, string>;
  materials: string[];
  care: string[];
  stock: number;
}

const sampleDetails: ProductDetails = {
  id: 1,
  name: "Shoes Reebok Zig Kinetica 3",
  price: 199.00,
  image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
  description: "High-performance running shoes with advanced cushioning technology",
  rating: 4.8,
  reviews: 42,
  stock: 15,
  sizes: ['40.5', '41', '42', '43', '43.5', '44', '44.5', '45'],
  features: [
    "Advanced cushioning technology",
    "Breathable mesh upper",
    "Durable rubber outsole",
    "Responsive energy return",
    "Lightweight design"
  ],
  specifications: {
    "Brand": "Reebok",
    "Model": "Zig Kinetica 3",
    "Weight": "280g (Size 42)",
    "Drop": "10mm",
    "Arch Support": "Neutral",
    "Closure": "Lace-up"
  },
  materials: [
    "Breathable mesh upper",
    "EVA foam midsole",
    "Rubber outsole",
    "Recycled materials in upper (20%)"
  ],
  care: [
    "Clean with a soft brush or cloth",
    "Hand wash with mild soap if needed",
    "Air dry at room temperature",
    "Avoid direct sunlight or heat",
    "Store in a cool, dry place"
  ],
}

const renderStars = (rating: number) => {
  const stars = [];
  const roundedRating = Math.round(rating * 2) / 2; // Round to nearest 0.5

  for (let i = 1; i <= 5; i++) {
    if (i <= roundedRating) {
      stars.push(<span key={i} className="star filled">★</span>);
    } else if (i - 0.5 === roundedRating) {
      stars.push(<span key={i} className="star half-filled">★</span>);
    } else {
      stars.push(<span key={i} className="star">★</span>);
    }
  }

  return stars;
};

const ProductDetails = () => {
  console.log('ProductDetails component rendering');
  const { id } = useParams();
  console.log('Product ID:', id);
  const { addToCart } = useCart();
  const [selectedSize, setSelectedSize] = useState<string>("");
  const [selectedTab, setSelectedTab] = useState<'details' | 'reviews' | 'discussion'>('reviews');
  
  // Add these state variables
  const [product, setProduct] = useState<ProductDetails>(sampleDetails);
  
  // Add state for reviews
  const [reviews, setReviews] = useState<Review[]>([
    {
      id: 1,
      user: "Helen M",
      rating: 5,
      comment: "Excellent running shoes. It feels very sturdy on the foot.",
      date: "Yesterday"
    },
    {
      id: 2,
      user: "Ann G",
      rating: 4,
      comment: "Good shoes",
      date: "2 days ago"
    }
  ]);

  // Update getRatingDistribution to use reviews state
  const getRatingDistribution = (): RatingStats => {
    const distribution: RatingDistribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
    reviews.forEach(review => {
      distribution[review.rating]++;
    });
    const total = reviews.length;
    return { distribution, total };
  };

  const getAverageRating = (): number => {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + review.rating, 0);
    return Number((sum / reviews.length).toFixed(1));
  };

  const renderDetailsTab = () => (
    <div className="details-content">
      <section>
        <h3>Key Features</h3>
        <ul>
          {product.features.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>
      </section>

      <section className="specifications">
        <h3>Specifications</h3>
        <div className="specs-grid">
          {Object.entries(product.specifications).map(([key, value]) => (
            <div key={key} className="spec-item">
              <span className="spec-label">{key}</span>
              <span className="spec-value">{value}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="materials">
        <h3>Materials</h3>
        <ul>
          {product.materials.map((material, index) => (
            <li key={index}>{material}</li>
          ))}
        </ul>
      </section>

      <section className="care">
        <h3>Care Instructions</h3>
        <ul>
          {product.care.map((instruction, index) => (
            <li key={index}>{instruction}</li>
          ))}
        </ul>
      </section>
    </div>
  );

  const handleAddToCart = () => {
    if (!selectedSize) {
      alert('Please select a size');
      return;
    }

    // Check if stock is available
    if (product.stock <= 0) {
      alert('Product is out of stock');
      return;
    }

    // Add to cart
    addToCart({
      id: Number(id),
      name: product.name,
      size: selectedSize,
      price: product.price,
      image: product.image
    });

    // Decrease stock
    setProduct(prev => ({
      ...prev,
      stock: prev.stock - 1
    }));
  };

  const handleReviewSubmit = ({ rating, comment }: { rating: number; comment: string }) => {
    // Here you would typically send the review to your backend
    const newReview: Review = {
      id: reviews.length + 1,
      user: "Current User", // Replace with actual user name from auth
      rating,
      comment,
      date: "Just now"
    };

    // For now, we'll just add it to the local state
    setReviews([newReview, ...reviews]);
  };

  const handleSearch = (query: string) => {
    // Handle search in product details if needed
    console.log('Search in product details:', query);
  };

  // Helper function to get stock status text and color
  const getStockStatus = (stock: number) => {
    if (stock === 0) return {
      text: 'Out of stock',
      className: 'out-of-stock'
    };
    if (stock <= 5) return {
      text: `${stock} items left in stock`,
      className: 'low-stock'
    };
    return {
      text: `${stock} items in stock`,
      className: 'in-stock'
    };
  };

  return (
    <div className="product-details-page">
      <Navbar onSearch={handleSearch} />
      
      <div className="product-container">
        {/* Simplified left column */}
        <div className="product-images">
          <div className="main-image">
            <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e" alt="Product" />
          </div>
        </div>

        {/* Simplified right column */}
        <div className="product-info">
          <h1>Shoes Reebok Zig Kinetica 3</h1>
          
          <div className="rating-summary">
            <div className="stars">{renderStars(4.8)}</div>
            <span>(42 reviews)</span>
          </div>

          <div className="price">Price: $199.00</div>

          {/* Simplified size selection */}
          <div className="size-selection">
            <h3>Select Size:</h3>
            <div className="size-options">
              {product.sizes.map(size => (
                <div key={size} className="size-option-container">
                  <button
                    className={`size-btn ${selectedSize === size ? 'selected' : ''} ${
                      product.stock === 0 ? 'out-of-stock' : ''
                    }`}
                    onClick={() => setSelectedSize(size)}
                    disabled={product.stock === 0}
                  >
                    {size}
                  </button>
                </div>
              ))}
            </div>
            {!selectedSize && <p className="size-error">Please select a size</p>}
          </div>

          <div className={`stock-status ${getStockStatus(product.stock).className}`}>
            {getStockStatus(product.stock).text}
          </div>

          <button 
            className="add-to-cart-btn" 
            onClick={handleAddToCart}
            disabled={!selectedSize}
          >
            Add to Cart
          </button>
        </div>
      </div>

      {/* Simplified tabs */}
      <div className="product-tabs">
        <div className="tab-headers">
          <button 
            onClick={() => setSelectedTab('details')}
            style={{
              fontWeight: selectedTab === 'details' ? 'bold' : 'normal',
              textDecoration: selectedTab === 'details' ? 'underline' : 'none'
            }}
          >
            Product Details
          </button>
          <button 
            onClick={() => setSelectedTab('reviews')}
            style={{
              fontWeight: selectedTab === 'reviews' ? 'bold' : 'normal',
              textDecoration: selectedTab === 'reviews' ? 'underline' : 'none'
            }}
          >
            Reviews
          </button>
        </div>

        <div className="tab-content">
          {selectedTab === 'details' && renderDetailsTab()}
          {selectedTab === 'reviews' && (
            <div className="reviews-section">
              <ReviewForm onSubmit={handleReviewSubmit} />
              
              <div className="rating-distribution">
                <div className="overall-rating">
                  <h2>4.8</h2>
                  <div className="stars">{renderStars(4.8)}</div>
                  <p>Based on 41 reviews</p>
                </div>
                
                <div className="rating-bars">
                  {[5, 4, 3, 2, 1].map(rating => {
                    const { distribution, total } = getRatingDistribution();
                    const percentage = (distribution[rating] / total) * 100;
                    
                    return (
                      <div key={rating} className="rating-bar">
                        <span>{rating}★</span>
                        <div className="bar-container">
                          <div className="bar" style={{ width: `${percentage}%` }}></div>
                        </div>
                        <span>{distribution[rating]}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="reviews-list">
                {reviews.map(review => (
                  <div key={review.id} className="review-item">
                    <div className="review-header">
                      <span className="user">{review.user}</span>
                      <span className="date">{review.date}</span>
                    </div>
                    <div className="stars">{renderStars(review.rating)}</div>
                    <p className="comment">{review.comment}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductDetails; 