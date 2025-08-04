import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { FaCoffee, FaSignOutAlt, FaBoxes, FaTags, FaBox, FaChartBar } from 'react-icons/fa';

const Layout = ({ children }) => {
  const { logout, username } = useAuth();
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: FaCoffee },
    { path: '/stock', label: 'Stock Management', icon: FaBoxes },
    { path: '/categories', label: 'Categories', icon: FaTags },
    { path: '/items', label: 'Items', icon: FaBox },
    { path: '/analytics', label: 'Analytics', icon: FaChartBar },
  ];

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <div style={{
        width: '250px',
        backgroundColor: '#2c3e50',
        color: 'white',
        padding: '20px 0',
        boxShadow: '2px 0 5px rgba(0,0,0,0.1)'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <FaCoffee size={32} style={{ marginBottom: '10px' }} />
          <h2 style={{ margin: '0', fontSize: '20px' }}>Stocker</h2>
          <p style={{ margin: '5px 0 0 0', fontSize: '12px', opacity: 0.8 }}>
            Cafe Inventory
          </p>
        </div>

        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '12px 20px',
                  color: isActive ? '#3498db' : 'white',
                  textDecoration: 'none',
                  backgroundColor: isActive ? 'rgba(52, 152, 219, 0.1)' : 'transparent',
                  borderLeft: isActive ? '3px solid #3498db' : '3px solid transparent',
                  transition: 'all 0.3s ease'
                }}
              >
                <Icon style={{ marginRight: '10px' }} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div style={{ marginTop: 'auto', padding: '20px' }}>
          <div style={{ marginBottom: '10px', fontSize: '12px', opacity: 0.8 }}>
            Logged in as: {username}
          </div>
          <button
            onClick={logout}
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              padding: '10px 15px',
              backgroundColor: 'transparent',
              border: '1px solid rgba(255,255,255,0.3)',
              color: 'white',
              borderRadius: '4px',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            <FaSignOutAlt style={{ marginRight: '8px' }} />
            Logout
          </button>
        </div>
      </div>

      {/* Main content */}
      <div style={{ flex: 1, backgroundColor: '#f5f5f5' }}>
        <div className="container">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout; 