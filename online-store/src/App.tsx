import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import SyncCart from './components/SyncCart';


// Customer routes
import Products from './pages/customers/Products';
import ProductDetails from './pages/customers/ProductDetails';
import Cart from './pages/customers/Cart';
import Checkout from './pages/customers/Checkout';
import Refund from './pages/customers/Refund';
import OrdersPage from './pages/customers/Orders';
import Login from './pages/auth/Login';
import SignUp from './pages/auth/Signup';
import WishlistPage from './pages/customers/WishlistPage';

// PM routes

import CommentsRatings from './pages/comments-ratings/CommentsRatings';
import ProtectedRoute from './components/ProtectedRoute';
import ProductManagerPanel from './pages/product-manager/ProductManagerPanel';
import ManageProducts from './pages/product-manager/ManageProducts';
import ApproveComments from './pages/product-manager/ApproveComments';
import ManageOrders from './pages/product-manager/ManageOrders';
import ViewInvoices from './pages/product-manager/ViewInvoices';
import Unauthorized from './pages/Unauthorized';

// SM routes


import ProtectedRouteSM from './components/ProtectedRoute';
import SalesManagerPanel from './pages/sales-manager/SalesManagerPanel';
import ManageSales from './pages/sales-manager/ManageSales';
import ViewInvoicesSM from './pages/sales-manager/ViewInvoicesSM';
import UnauthorizedSM from './pages/Unauthorized';
import ManagePrices from './pages/sales-manager/ManagePrices';
import RevenueReport from './pages/sales-manager/RevenueReport';
import ManageCategories from './pages/product-manager/ManageCategories';
function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <SyncCart />
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
            <Route path="/wishlist" element={<WishlistPage />} />
            <Route path="/unauthorized" element={<Unauthorized />} />
            {/* PM routes - add a prefix to distinguish them */}
            <Route
              path="/product-manager"
              element={
                <ProtectedRoute allowedRoles={['Product Manager']}>
                  <ProductManagerPanel />
                </ProtectedRoute>
              }
            >
              <Route path="products" element={<ManageProducts />} />
              <Route path="categories" element={<ManageCategories />} />
              <Route path="comments" element={<ApproveComments />} />
              <Route path="orders" element={<ManageOrders />} />
              <Route path="invoices" element={<ViewInvoices />} />
            </Route>
              {/* PM routes - add a prefix to distinguish them */}
            <Route
              path="/sales-manager"
              /*element={
                <ProtectedRoute allowedRoles={['Sales Manager']}>
                  <ProductManagerPanel />
                </ProtectedRoute>
              }*/
                element={<SalesManagerPanel />}
              
            >
              <Route path="products" element={<ManageSales />} />
              </Route>
            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/products" replace />} />
            <Route path="/sales-panel" element={<SalesManagerPanel />}>
            <Route path="manage-prices" element={<ManagePrices />} />
            <Route path="view-invoices" element={<ViewInvoicesSM />} />
            <Route path="revenue-report" element={<RevenueReport />} />
            </Route>
          </Routes>
        </div>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;