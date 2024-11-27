import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const mockUsers: { email: string; password: string }[] = [];

const SignUp = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    // Check if the user already exists
    const userExists = mockUsers.some((user) => user.email === email);
    if (userExists) {
      setError('User already exists');
      setIsLoading(false);
      return;
    }

    // Simulate user registration
    mockUsers.push({ email, password });
    console.log('Registered users:', mockUsers); // To see the registered users
    setTimeout(() => {
      setIsLoading(false);
      navigate('/login'); // Redirect to login after successful registration
    }, 1000); // Simulate a network delay
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Create an Account</h2>

        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label>Email address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
            />
          </div>

          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
            />
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading ? 'Signing up...' : 'Sign up'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignUp;
