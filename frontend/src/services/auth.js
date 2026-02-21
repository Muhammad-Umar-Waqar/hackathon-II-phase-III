import { authAPI } from './api';

class AuthService {
  /**
   * Register a new user
   */
  static async register(userData) {
    try {
      const response = await authAPI.register(userData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Login user and store token
   */
  static async login(email, password) {
    try {
      const response = await authAPI.login(email, password);

      // Store token and user data in localStorage
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data));
      }

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Logout user and clear stored data
   */
  static logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  /**
   * Get current authenticated user
   */
  static async getCurrentUser() {
    try {
      const response = await authAPI.getCurrentUser();
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  /**
   * Get stored user data
   */
  static getUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  }

  /**
   * Get auth token
   */
  static getToken() {
    return localStorage.getItem('access_token');
  }

  /**
   * Check if token is expired
   */
  static isTokenExpired(token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      return true; // If we can't parse the token, treat it as expired
    }
  }

  /**
   * Refresh the access token
   */
  static async refreshToken() {
    // In a real implementation, you would call your refresh endpoint
    // For now, we'll just redirect to login if the token is expired
    const token = this.getToken();
    if (token && this.isTokenExpired(token)) {
      this.logout();
      throw new Error('Token expired. Please login again.');
    }
  }

  /**
   * Handle API errors
   */
  static handleError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - clear auth data
        this.logout();
        return new Error('Unauthorized. Please login again.');
      } else if (status === 409) {
        // Conflict - typically duplicate email/username
        return new Error(data.detail || 'User already exists');
      } else if (status >= 500) {
        // Server error
        return new Error('Server error. Please try again later.');
      } else {
        // Other client errors
        return new Error(data.detail || 'Request failed');
      }
    } else if (error.request) {
      // Request was made but no response received
      return new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      return new Error(error.message || 'An unexpected error occurred.');
    }
  }
}

export default AuthService;