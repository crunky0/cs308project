import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import ProductList from './components/ProductList';
import Footer from './components/Footer';
import Cart from './components/Cart';
import AuthPage from './components/AuthPage';
import ProductPage from './components/ProductPage';

function App() {
  const [products, setProducts] = useState([]);
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const mockProducts = [
      {
        id: 1,
        name: "Smartphone",
        description: "Latest model smartphone with great features",
        price: 999.99,
      },
      {
        id: 2,
        name: "Laptop",
        description: "High-performance laptop for work and play",
        price: 1299.99,
      },
      {
        id: 3,
        name: "Headphones",
        description: "Noise-cancelling wireless headphones",
        price: 199.99,
      },
    ];

    setTimeout(() => {
      setProducts(mockProducts);
    }, 1000);
  }, []);

  const handleAddToCart = (product) => {
    setCartItems([...cartItems, product]);
  };

  return (
    <Router>
      <div style={appStyle}>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<ProductList products={products} onAddToCart={handleAddToCart} />} />
            <Route path="/cart" element={<Cart cartItems={cartItems} />} />
            <Route path="/auth" element={<AuthPage />} />
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
