import React, { useState } from 'react';

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div style={authPageStyle}>
      <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
      <form style={formStyle}>
        {!isLogin && (
          <div>
            <label>Username:</label>
            <input type="text" placeholder="Enter your username" required />
          </div>
        )}
        <div>
          <label>Email:</label>
          <input type="email" placeholder="Enter your email" required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" placeholder="Enter your password" required />
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

const formStyle = {
  display: 'inline-block',
  textAlign: 'left',
};

const buttonStyle = {
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  margin: '10px 0',
  cursor: 'pointer',
};

const toggleButtonStyle = {
  backgroundColor: 'transparent',
  color: '#007BFF',
  border: 'none',
  textDecoration: 'underline',
  cursor: 'pointer',
};

export default AuthPage;
