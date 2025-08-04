import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { FaCoffee, FaUser, FaLock } from 'react-icons/fa';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Normalize username to lowercase
    const normalizedUsername = username.toLowerCase().trim();

    if (!normalizedUsername || !password) {
      setError('Username and password are required');
      return;
    }

    try {
      const success = isRegistering 
        ? await register(normalizedUsername, password)
        : await login(normalizedUsername, password);
      
      if (success) {
        // Login/Register successful - redirect will be handled by App.js
      } else {
        setError(isRegistering ? 'Registration failed' : 'Invalid username or password');
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'An error occurred');
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
              placeholder="Enter username (will be converted to lowercase)"
              required
            />
            <small style={{ color: '#666', fontSize: '12px' }}>
              Username will be converted to lowercase automatically
            </small>
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
            {isRegistering ? 'Register' : 'Login'}
          </button>
        </form>

        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          <button
            type="button"
            onClick={() => setIsRegistering(!isRegistering)}
            style={{
              background: 'none',
              border: 'none',
              color: '#007bff',
              textDecoration: 'underline',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            {isRegistering ? 'Already have an account? Login' : 'Need an account? Register'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login; 