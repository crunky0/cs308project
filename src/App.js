import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Header from './components/Header';
import ProductList from './components/ProductList';
import Footer from './components/Footer';
import Cart from './components/Cart';
import AuthPage from './components/AuthPage';
import MyOrders from './components/MyOrders';
import ProductPage from './components/ProductPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status
  const [cartItems, setCartItems] = useState([]); // Store cart items

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCartItems([]); // Clear the cart on logout
  };

  const addToCart = (product) => {
    setCartItems([...cartItems, product]);
  };

  return (
    <Router>
      <div style={appStyle}>
        <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
        <main>
          <Routes>
            <Route
              path="/auth"
              element={<AuthPage onLogin={handleLogin} />}
            />
            <Route
              path="/"
              element={<ProductList onAddToCart={addToCart} />}
            />
            <Route
              path="/cart"
              element={
                <Cart
                  cartItems={cartItems}
                  isLoggedIn={isLoggedIn}
                  onLoginRedirect={() => setIsLoggedIn(true)}
                />
              }
            />
            <Route path="/my-orders" element={isLoggedIn ? <MyOrders /> : <AuthPage onLogin={handleLogin} />} />
            <Route path="/product/:productId" element={<ProductPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

const appStyle = {
  fontFamily: 'Arial, sans-serif',
  margin: '0',
  padding: '0',
  minHeight: '100vh',
  position: 'relative',
};

export default App;
