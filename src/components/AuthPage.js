import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AuthPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email && password && (isLogin || username)) {
      alert(`${isLogin ? 'Login' : 'Signup'} Successful!`);
      onLogin(); // Call the onLogin function to update the login state
      navigate('/'); // Redirect to the main page
    } else {
      alert('Please fill in all required fields!');
    }
  };

  return (
    <div style={authPageStyle}>
      <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
      <form onSubmit={handleSubmit} style={formStyle}>
        {!isLogin && (
          <div style={inputGroupStyle}>
            <label>Username:</label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required={!isLogin}
              style={inputStyle}
            />
          </div>
        )}
        <div style={inputGroupStyle}>
          <label>Email:</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={inputStyle}
          />
        </div>
        <div style={inputGroupStyle}>
          <label>Password:</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={inputStyle}
          />
        </div>
        <button type="submit" style={buttonStyle}>
          {isLogin ? 'Login' : 'Sign Up'}
        </button>
      </form>
      <button style={toggleButtonStyle} onClick={toggleAuthMode}>
        {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Login'}
      </button>
    </div>
  );
}

const authPageStyle = {
  textAlign: 'center',
  margin: '20px',
  padding: '20px',
};

// Styles (same as previous AuthPage)
const formStyle = { /* same styles as before */ };
const inputGroupStyle = { /* same styles as before */ };
const inputStyle = { /* same styles as before */ };
const buttonStyle = { /* same styles as before */ };
const toggleButtonStyle = { /* same styles as before */ };

export default AuthPage;
