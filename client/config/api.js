/**
 * Centralized API Configuration
 * All API-related configuration should be defined here
 */

// API Configuration
export const API_CONFIG = {
  // Base URL for all API calls
  BASE_URL: 'http://127.0.0.1:8003',
  
  // Timeout settings
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
  
  // Endpoints
  ENDPOINTS: {
    // Authentication
    LOGIN: '/users/login',
    REGISTER: '/users/register',
    
    // Users
    USERS: '/users/',
    USER_PREFERENCES: '/users/me/preferences',
    
    // Books
    BOOKS: '/books/',
    BOOK_UPLOAD: '/books/upload',
    BOOK_JOB_STATUS: '/books/jobs/{job_id}/status',
    BOOK_JOB_RESULT: '/books/jobs/{job_id}/result',
    BOOK_MARKUP: '/books/{book_id}/markup',
    
    // Analytics
    ANALYTICS_EVENTS: '/analytics/events',
    
    // Health
    HEALTH: '/',
  },
  
  // Headers
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
  },
};

// Helper function to build full URL
export const buildApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Helper function to replace URL parameters
export const buildUrlWithParams = (endpoint, params) => {
  let url = endpoint;
  Object.keys(params).forEach(key => {
    url = url.replace(`{${key}}`, params[key]);
  });
  return buildApiUrl(url);
};

export default API_CONFIG;
