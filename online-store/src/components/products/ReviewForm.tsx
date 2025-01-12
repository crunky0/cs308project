import React, { useState } from 'react';
import './ReviewForm.css';

interface ReviewFormProps {
  onSubmit: (review: { rating: number; comment: string }) => void;
}

const ReviewForm: React.FC<ReviewFormProps> = ({ onSubmit }) => {
  const [rating, setRating] = useState<number>(0);
  const [comment, setComment] = useState<string>('');
  const [hoveredStar, setHoveredStar] = useState<number>(0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (rating === 0) {
      alert('Please select a rating');
      return;
    }
    onSubmit({ rating, comment });
    setRating(0);
    setComment('');
  };

  return (
    <form className="review-form" onSubmit={handleSubmit}>
      <h3>Write a Review</h3>
      
      <div className="rating-input">
  <p>Rate this product:</p>
  <div className="stars-input">
    {Array.from({ length: 5 }).map((_, index) => {
      const fullValue = index + 1; // Value for full star
      const halfValue = index + 0.5; // Value for half star

      return (
        <span
          key={index}
          className={`star ${
            hoveredStar >= fullValue || rating >= fullValue
              ? 'full'
              : hoveredStar >= halfValue || rating >= halfValue
              ? 'half'
              : 'empty'
          }`}
          onClick={() =>
            setRating(hoveredStar >= halfValue && hoveredStar < fullValue ? halfValue : fullValue)
          }
          onMouseEnter={() =>
            setHoveredStar(hoveredStar >= halfValue && hoveredStar < fullValue ? halfValue : fullValue)
          }
          onMouseLeave={() => setHoveredStar(0)}
        >
          ★
        </span>
      );
    })}
  </div>
</div>

      <div className="comment-input">
        <textarea
          placeholder="Share your thoughts about this product..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          required
          rows={4}
        />
      </div>

      <button type="submit" className="submit-review-btn">
        Submit Review
      </button>
    </form>
  );
};

export default ReviewForm; 