import { Routes, Route } from 'react-router-dom';
import Login from '../pages/auth/Login';
import Products from '../pages/customers/Products';
import ProtectedRoute from '../components/ProtectedRoute';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/products"
        element={
          <ProtectedRoute>
            <Products />
          </ProtectedRoute>
        }
      />
      {/* Add more routes as needed */}
    </Routes>
  );
};

export default AppRoutes; 