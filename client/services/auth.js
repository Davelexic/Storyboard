/**
 * Authentication Service for Cinematic Reading Engine
 * Handles user authentication, token management, and session persistence
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from './api';

// Storage keys
const STORAGE_KEYS = {
  AUTH_TOKEN: 'cinei_auth_token',
  USER_DATA: 'cinei_user_data',
  REMEMBER_ME: 'cinei_remember_me',
};

/**
 * Authentication Service
 */
class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
    this.token = null;
  }

  /**
   * Initialize authentication state from storage
   */
  async initialize() {
    try {
      const token = await AsyncStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
      const userData = await AsyncStorage.getItem(STORAGE_KEYS.USER_DATA);
      
      if (token && userData) {
        this.token = token;
        this.user = JSON.parse(userData);
        this.isAuthenticated = true;
        apiClient.setToken(token);
        return true;
      }
    } catch (error) {
      console.error('Failed to initialize auth:', error);
      await this.logout();
    }
    
    return false;
  }

  /**
   * Login user with email and password
   */
  async login(email, password, rememberMe = false) {
    try {
      const response = await apiClient.login(email, password);
      
      // Store authentication data
      this.token = response.access_token;
      this.isAuthenticated = true;
      
      // Extract user data from token (if available)
      // In a real app, you might want to decode the JWT token
      this.user = { email };
      
      // Save to storage
      await AsyncStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, this.token);
      await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(this.user));
      await AsyncStorage.setItem(STORAGE_KEYS.REMEMBER_ME, JSON.stringify(rememberMe));
      
      return {
        success: true,
        user: this.user,
        token: this.token,
      };
    } catch (error) {
      console.error('Login failed:', error);
      throw new Error(error.message || 'Login failed');
    }
  }

  /**
   * Register new user
   */
  async register(email, password) {
    try {
      const response = await apiClient.register(email, password);
      return {
        success: true,
        message: 'Registration successful',
      };
    } catch (error) {
      console.error('Registration failed:', error);
      throw new Error(error.message || 'Registration failed');
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      // Clear authentication state
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      
      // Clear API client token
      apiClient.clearToken();
      
      // Clear storage
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.AUTH_TOKEN,
        STORAGE_KEYS.USER_DATA,
        STORAGE_KEYS.REMEMBER_ME,
      ]);
      
      return { success: true };
    } catch (error) {
      console.error('Logout failed:', error);
      // Even if storage clear fails, clear memory state
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      apiClient.clearToken();
      throw error;
    }
  }

  /**
   * Check if user is authenticated
   */
  isLoggedIn() {
    return this.isAuthenticated && !!this.token;
  }

  /**
   * Get current user
   */
  getCurrentUser() {
    return this.user;
  }

  /**
   * Get current token
   */
  getToken() {
    return this.token;
  }

  /**
   * Refresh authentication (if needed)
   */
  async refreshAuth() {
    if (!this.token) {
      return false;
    }
    
    try {
      // Test the token by making a simple API call
      await apiClient.healthCheck();
      return true;
    } catch (error) {
      console.error('Token validation failed:', error);
      await this.logout();
      return false;
    }
  }

  /**
   * Update user data
   */
  async updateUserData(userData) {
    this.user = { ...this.user, ...userData };
    await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(this.user));
  }

  /**
   * Get remember me preference
   */
  async getRememberMe() {
    try {
      const rememberMe = await AsyncStorage.getItem(STORAGE_KEYS.REMEMBER_ME);
      return rememberMe ? JSON.parse(rememberMe) : false;
    } catch (error) {
      console.error('Failed to get remember me preference:', error);
      return false;
    }
  }

  /**
   * Set remember me preference
   */
  async setRememberMe(rememberMe) {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.REMEMBER_ME, JSON.stringify(rememberMe));
    } catch (error) {
      console.error('Failed to set remember me preference:', error);
    }
  }
}

// Create and export singleton instance
const authService = new AuthService();

export default authService;
export { STORAGE_KEYS };
