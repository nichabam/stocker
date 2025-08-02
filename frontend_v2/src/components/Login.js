import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { FaCoffee, FaUser, FaLock } from 'react-icons/fa';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, CAFE_USERNAME, CAFE_PASSWORD } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (login(username, password)) {
      // Login successful - redirect will be handled by App.js
    } else {
      setError('Invalid username or password');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <FaCoffee size={48} style={{ color: '#007bff', marginBottom: '10px' }} />
          <h1 style={{ color: '#333', marginBottom: '5px' }}>☕ Stocker</h1>
          <p style={{ color: '#666' }}>Cafe Inventory Management</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">
              <FaUser style={{ marginRight: '8px' }} />
              Username
            </label>
            <input
              type="text"
              id="username"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <FaLock style={{ marginRight: '8px' }} />
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          {error && (
            <div className="alert alert-danger">
              ❌ {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
            Login
          </button>
        </form>

        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          <h4 style={{ marginBottom: '10px', fontSize: '14px' }}>ℹ️ Login Credentials</h4>
          <p style={{ margin: '5px 0', fontSize: '12px' }}>
            <strong>Username:</strong> {CAFE_USERNAME}
          </p>
          <p style={{ margin: '5px 0', fontSize: '12px' }}>
            <strong>Password:</strong> {CAFE_PASSWORD}
          </p>
          <p style={{ margin: '10px 0 0 0', fontSize: '11px', color: '#666' }}>
            These credentials are for cafe staff use only.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login; 