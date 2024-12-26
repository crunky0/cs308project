import React, { useState, useEffect } from 'react';

const ApproveComments = () => {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    // Fetch unapproved comments from API
    const fetchComments = async () => {
      const response = await fetch('/api/comments/unapproved');
      const data = await response.json();
      setComments(data);
    };
    fetchComments();
  }, []);

  const handleApprove = async (commentId: number) => {
    // API call to approve comment
    // Update state to remove approved comment
  };

  return (
    <div>
      <h2>Approve Comments</h2>
      <ul>
        {comments.map(comment => (
          <li key={comment.id}>
            <p>{comment.text}</p>
            <button onClick={() => handleApprove(comment.id)}>Approve</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ApproveComments;