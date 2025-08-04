import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../utils/apiClient';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(true);

  const login = async (inputUsername, inputPassword) => {
    try {
      const response = await apiClient.login(inputUsername, inputPassword);
      if (response && response.access_token) {
        setIsAuthenticated(true);
        setUsername(inputUsername);
        setToken(response.access_token);
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('username', inputUsername);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUsername('');
    setToken('');
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  };

  const register = async (inputUsername, inputPassword) => {
    try {
      const response = await apiClient.register(inputUsername, inputPassword);
      if (response && response.message) {
        return true;
      }
      return false;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUsername = localStorage.getItem('username');
    
    if (storedToken && storedUsername) {
      // Verify token is still valid
      apiClient.verifyToken(storedToken).then(isValid => {
        if (isValid) {
          setIsAuthenticated(true);
          setUsername(storedUsername);
          setToken(storedToken);
        } else {
          logout();
        }
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const value = {
    isAuthenticated,
    username,
    token,
    login,
    logout,
    register,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 