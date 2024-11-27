import React, { useState } from 'react';
import Sidebar from '../../components/pm/layout/Sidebar';
import Navbar from '../../components/pm/layout/Navbar';
import './CommentsRatings.css';

// Add new interface for comment data
interface CommentData {
  id: string;
  name: string;
  comment: string;
  rating: number;
  date: string;
  productId: string;
}

const CommentsRatings: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState<CommentData | null>(null);

  const handleView = (comment: CommentData) => {
    setSelectedComment(comment);
    setIsModalOpen(true);
  };

  return (
    <div className="admin-layout">
      <Navbar 
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
      />
      <div className={`main-container ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
        <div className="content-wrapper">
          <h1 className="">Comments & Ratings</h1>
          <div className="data-sheet">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Product ID</th>
                  <th>Comment</th>
                  <th>Rating</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>001</td>
                  <td>John Doe</td>
                  <td>PRD-123</td>
                  <td>Great service, very professional!</td>
                  <td>
                    <div className="rating">★★★★☆</div>
                  </td>
                  <td>2024-03-20</td>
                  <td>
                    <button className="action-button" onClick={() => handleView({
                      id: '001',
                      name: 'John Doe',
                      comment: 'Great service, very professional!',
                      rating: 4,
                      date: '2024-03-20',
                      productId: 'PRD-123'
                    })}>View</button>
                    <button className="action-button approve">Approve</button>
                    <button className="action-button reject">Reject</button>
                    <button className="action-button">Delete</button>
                  </td>
                </tr>
                <tr>
                  <td>002</td>
                  <td>Sarah Smith</td>
                  <td>PRD-456</td>
                  <td>Quick delivery and excellent product quality.</td>
                  <td>
                    <div className="rating">★★★★★</div>
                  </td>
                  <td>2024-03-19</td>
                  <td>
                    <button className="action-button" onClick={() => handleView({
                      id: '002',
                      name: 'Sarah Smith',
                      comment: 'Quick delivery and excellent product quality.',
                      rating: 5,
                      date: '2024-03-19',
                      productId: 'PRD-456'
                    })}>View</button>
                    <button className="action-button approve">Approve</button>
                    <button className="action-button reject">Reject</button>
                    <button className="action-button">Delete</button>
                  </td>
                </tr>
                <tr>
                  <td>003</td>
                  <td>Mike Johnson</td>
                  <td>PRD-789</td>
                  <td>Could be better. Delivery was delayed.</td>
                  <td>
                    <div className="rating">★★★☆☆</div>
                  </td>
                  <td>2024-03-18</td>
                  <td>
                    <button className="action-button" onClick={() => handleView({
                      id: '003',
                      name: 'Mike Johnson',
                      comment: 'Could be better. Delivery was delayed.',
                      rating: 3,
                      date: '2024-03-18',
                      productId: 'PRD-789'
                    })}>View</button>
                    <button className="action-button approve">Approve</button>
                    <button className="action-button reject">Reject</button>
                    <button className="action-button">Delete</button>
                  </td>
                </tr>
                <tr>
                  <td>004</td>
                  <td>Emma Wilson</td>
                  <td>PRD-234</td>
                  <td>Amazing experience! Will definitely order again.</td>
                  <td>
                    <div className="rating">★★★★★</div>
                  </td>
                  <td>2024-03-18</td>
                  <td>
                    <button className="action-button" onClick={() => handleView({
                      id: '004',
                      name: 'Emma Wilson',
                      comment: 'Amazing experience! Will definitely order again.',
                      rating: 5,
                      date: '2024-03-18',
                      productId: 'PRD-234'
                    })}>View</button>
                    <button className="action-button approve">Approve</button>
                    <button className="action-button reject">Reject</button>
                    <button className="action-button">Delete</button>
                  </td>
                </tr>
                <tr>
                  <td>005</td>
                  <td>David Brown</td>
                  <td>PRD-567</td>
                  <td>Good product but packaging needs improvement.</td>
                  <td>
                    <div className="rating">★★★★☆</div>
                  </td>
                  <td>2024-03-17</td>
                  <td>
                    <button className="action-button" onClick={() => handleView({
                      id: '005',
                      name: 'David Brown',
                      comment: 'Good product but packaging needs improvement.',
                      rating: 4,
                      date: '2024-03-17',
                      productId: 'PRD-567'
                    })}>View</button>
                    <button className="action-button approve">Approve</button>
                    <button className="action-button reject">Reject</button>
                    <button className="action-button">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {isModalOpen && selectedComment && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button className="modal-close" onClick={() => setIsModalOpen(false)}>×</button>
            <h2>Comment Details</h2>
            <div className="modal-body">
              <p><strong>ID:</strong> {selectedComment.id}</p>
              <p><strong>Name:</strong> {selectedComment.name}</p>
              <p><strong>Product ID:</strong> <a href={`/products/${selectedComment.productId}`}>{selectedComment.productId}</a></p>
              <p><strong>Date:</strong> {selectedComment.date}</p>
              <p><strong>Rating:</strong> {'★'.repeat(selectedComment.rating)}{'☆'.repeat(5-selectedComment.rating)}</p>
              <p><strong>Comment:</strong> {selectedComment.comment}</p>
            </div>
            <div className="modal-actions">
              <button className="accept-button" onClick={() => setIsModalOpen(false)}>Approve</button>
              <button className="reject-button" onClick={() => setIsModalOpen(false)}>Reject</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CommentsRatings;