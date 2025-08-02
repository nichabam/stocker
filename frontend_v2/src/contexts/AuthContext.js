import React, { createContext, useContext, useState, useEffect } from 'react';

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

  // Simple authentication for single cafe (replicating Streamlit auth)
  const CAFE_USERNAME = 'cafe';
  const CAFE_PASSWORD = 'stock2024';

  const login = (inputUsername, inputPassword) => {
    if (inputUsername === CAFE_USERNAME && inputPassword === CAFE_PASSWORD) {
      setIsAuthenticated(true);
      setUsername(inputUsername);
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('username', inputUsername);
      return true;
    }
    return false;
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUsername('');
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
  };

  useEffect(() => {
    const storedAuth = localStorage.getItem('isAuthenticated');
    const storedUsername = localStorage.getItem('username');
    
    if (storedAuth === 'true' && storedUsername) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
    }
  }, []);

  const value = {
    isAuthenticated,
    username,
    login,
    logout,
    CAFE_USERNAME,
    CAFE_PASSWORD,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 