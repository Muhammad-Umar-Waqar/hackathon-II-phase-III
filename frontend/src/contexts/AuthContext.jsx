import React, { createContext, useContext, useState, useEffect } from 'react';
import AuthService from '../services/auth';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on initial load
    const checkAuthStatus = async () => {
      try {
        const storedUser = AuthService.getUser();
        if (storedUser) {
          // Verify token is still valid by making a request to get user info
          const currentUser = await AuthService.getCurrentUser();
          setUser(currentUser);
        }
      } catch (error) {
        // Token is invalid, clear stored data
        AuthService.logout();
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email, password) => {
    const userData = await AuthService.login(email, password);
    setUser(userData);
    return userData;
  };

  const register = async (userData) => {
    const newUser = await AuthService.register(userData);
    setUser(newUser);
    return newUser;
  };

  const logout = () => {
    AuthService.logout();
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};