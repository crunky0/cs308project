import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';

// Customer routes
import Products from './pages/customers/Products';
import ProductDetails from './pages/customers/ProductDetails';
import Cart from './pages/customers/Cart';
import Checkout from './pages/customers/Checkout';
import Refund from './pages/customers/Refund';
import OrdersPage from './pages/customers/Orders';
import Login from './pages/auth/Login';
import SignUp from './pages/auth/Signup';

// PM routes

import CommentsRatings from './pages/comments-ratings/CommentsRatings';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <div className="app-container">
          <Routes>
            {/* Customer routes */}
            <Route path="/" element={<Navigate to="/products" replace />} />
            <Route path="/products" element={<Products />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/product/:id" element={<ProductDetails />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/refund/:orderId" element={<Refund />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            {/* PM routes - add a prefix to distinguish them */}


            
            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/products" replace />} />
          </Routes>
        </div>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;