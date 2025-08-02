import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import CategoryManagement from './components/CategoryManagement';
import ItemManagement from './components/ItemManagement';
import StockManagement from './components/StockManagement';
import Analytics from './components/Analytics';
import Layout from './components/Layout';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/categories" element={<CategoryManagement />} />
          <Route path="/items" element={<ItemManagement />} />
          <Route path="/stock" element={<StockManagement />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/login" element={<Navigate to="/" />} />
        </Routes>
      </Layout>
    </Router>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
};

export default App; 